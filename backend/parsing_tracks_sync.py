import io
import logging
import os
from urllib.error import HTTPError

import requests
import tempfile
from requests import RequestException
from sclib import SoundcloudAPI, Track, Playlist
from PIL import Image
from storage3.exceptions import StorageApiError

from backend.config import SUPABASE_URL, SUPABASE_KEY, DEFAULT_COVER
from disk_to_db import save_track_to_db, save_cover_to_db
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type, before_sleep_log
import time
from supabase import Client, create_client

logging.basicConfig(level=logging.INFO, format='%(asctime)s -- %(levelname)s -- %(message)s')
logger = logging.getLogger(__name__)




def sanitize_path(text):
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
    }
    text = text.lower()
    for cyr, lat in translit_dict.items():
        text = text.replace(cyr, lat)
    return text

## получаем ссылку на supabase
def get_url(bucket_name, file_path):
    public_url = supabase.storage.from_(bucket_name).get_public_url(file_path)
    print(f"public_url: {public_url}")
    return public_url


## сохранение обложки
@retry(stop=stop_after_attempt(5),
                       wait=wait_fixed(3),
                   retry=retry_if_exception_type((RequestException, StorageApiError, HTTPError, ConnectionResetError)),
                       before_sleep=before_sleep_log(logger, logging.WARNING)
                    )
def save_cover(solo_track_id: str, artwork_url: str, solo_cover_path: str) -> str:
    try:
        response = requests.get(artwork_url)
        response.raise_for_status()

        upload_response = supabase.storage.from_("covers").upload(
            path=solo_cover_path,
            file=response.content
        )
        public_url = supabase.storage.from_("covers").get_public_url(solo_cover_path)
        cover_id = save_cover_to_db(solo_track_id, public_url)
        return cover_id
    except Exception as e:
        print(f"Error saving cover for track {solo_track_id}: {e}")
        raise

# сохранение трека в backblaze
@retry(stop=stop_after_attempt(5),
                       wait=wait_fixed(3),
                   retry=retry_if_exception_type((RequestException, StorageApiError, HTTPError, ConnectionResetError)),
                       before_sleep=before_sleep_log(logger, logging.WARNING)
                    )
def save_track(url, soundcloud_api):
    try:
        time.sleep(1)
        track = soundcloud_api.resolve(url)
        assert isinstance(track, Track), "URL is not managed to be a playlist"

        mp3_data = io.BytesIO()
        track.write_mp3_to(mp3_data)
        mp3_data.seek(0)

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as mp3_data_file:
            track.write_mp3_to(mp3_data_file)
            mp3_data_file.flush()
            temp_mp3_path = mp3_data_file.name

            track_artist_path = sanitize_path(track.artist)
            track_title_path = sanitize_path(track.title)

        with open(temp_mp3_path, "rb") as mp3_file:
            mp3_data = mp3_file.read()


        supabase_path = f"{track_artist_path}_{track_title_path}.mp3"
        track_bucket = "covers"
        supabase.storage.from_(track_bucket).upload(
            path=supabase_path,
            file=mp3_data,
            file_options={"content-type": "audio/mp3"}
        )
        os.remove(temp_mp3_path)

        download_url = get_url(track_bucket, supabase_path)
        track_id = save_track_to_db(track.title, download_url)
        mp3_data.close()

        return track_id

    except AssertionError as e:
        print(f"Error: url isnt a track: {e}")
        return None
    except requests.RequestException as e:
        print(f"Error: url isn't a track: {e}")
        return None
    except StorageApiError as e:
        print(f"eRROR WE CANT MANAGED THIS TRACK: {e}")
        return None
    except HTTPError as e:
        print(f"Error: url isn't a track: {e}")
        return None
# сохранение альбома в baclblazr

def save_album(url, soundcloud_api):
    """

    :type api: object
    """
    try:
        playlist = soundcloud_api.resolve(url)
        assert isinstance(playlist, Playlist), "URL is not managed to be a playlist"

        track_ids = []
        album_bucket = "tracks"

        for track in playlist.tracks:
            time.sleep(1)

            @retry(stop=stop_after_attempt(5),
                       wait=wait_fixed(3),
                   retry=retry_if_exception_type((RequestException, StorageApiError, HTTPError, ConnectionResetError)),
                       before_sleep=before_sleep_log(logger, logging.WARNING)
                    )
            def single_track():

                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
                    track.write_mp3_to(tmp_file)
                    tmp_file.flush()
                    temp_file_path = tmp_file.name

                    playlist_title_path = sanitize_path(playlist.title)
                    track_artist_path = sanitize_path(track.artist)
                    track_title_path = sanitize_path(track.title)
                    supabase_path = f"{playlist_title_path}/{track_artist_path}_{track_title_path}.mp3"

                with open(temp_file_path, "rb") as mp3_file:
                    mp3_data = mp3_file.read()

                supabase.storage.from_(album_bucket).upload(
                    path=supabase_path,
                    file=mp3_data,
                    file_options={"content-type": "audio/mp3"}
                )
                os.remove(temp_file_path)

                solo_download_url = get_url(album_bucket, supabase_path)

                solo_track_id = save_track_to_db(track.title, solo_download_url)

                solo_cover_path = f"{playlist.title}/{track.artist}_{track.title}.jpg"
                solo_cover_path = sanitize_path(solo_cover_path)
                time.sleep(1)
                solo_cover_id = save_cover(solo_track_id, track.artwork_url, solo_cover_path)

                return solo_track_id, solo_cover_id
            track_id = single_track()
            track_ids.append(track_id)

    except StorageApiError as e:
        logging.error(f"error by uploading the playlist: {e}")
        return []
    except HTTPError as e:
        logging.error(f"error by downloading the playlist: {e}")
        return []

    return track_ids

if __name__ == "__main__":
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    sc_api = SoundcloudAPI()
    urls = ["https://soundcloud.com/elizaveta-lavrova-108256826/sets/morgenshtern-golden-edition"]

    for one_url in urls:
        track_ids = save_album(one_url, sc_api)
        if track_ids:
            logging.info(f"saved {len(track_ids)} tracks")
        else:
            logging.warning(f"no tracks saved for {one_url}")
