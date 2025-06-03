import io
import logging
import os
from urllib.error import HTTPError
import time
import requests
import tempfile
from requests import RequestException
from sclib import SoundcloudAPI, Track, Playlist
from storage3.exceptions import StorageApiError
import disk_to_db, sanitizer
import tenacity
from supabase import Client, create_client
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s -- %(levelname)s -- %(message)s')
logger = logging.getLogger(__name__)
load_dotenv()

DEFAULT_COVER = os.getenv('DEFAULT_COVER')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')


## сохранение обложки
@tenacity.retry(stop=tenacity.stop_after_attempt(5),
                wait=tenacity.wait_fixed(3),
                retry=tenacity.retry_if_exception_type(
                    (RequestException, StorageApiError, HTTPError, ConnectionResetError)),
                before_sleep=tenacity.before_sleep_log(logger, logging.WARNING)
                )
# get high_quality
# pass

def save_cover(solo_track_id: str, artwork_url: str, solo_cover_path: str) -> str:
    if not artwork_url:
        cover_id = DEFAULT_COVER
        return cover_id

    try:

        high_quality_url = artwork_url.replace("large", "t500x500")

        response = requests.get(high_quality_url)
        response.raise_for_status()

        supabase.storage.from_("covers").upload(
            path=solo_cover_path,
            file=response.content
        )
        public_url = supabase.storage.from_("covers").get_public_url(solo_cover_path)
        cover_id = disk_to_db.save_cover_to_db(solo_track_id, public_url)
        return cover_id
    except Exception as e:
        print(f"Error saving cover for track {solo_track_id}: {e}")
        raise


# сохранение трека в backblaze
@tenacity.retry(stop=tenacity.stop_after_attempt(5),
                wait=tenacity.wait_fixed(3),
                retry=tenacity.retry_if_exception_type(
                    (RequestException, StorageApiError, HTTPError, ConnectionResetError)),
                before_sleep=tenacity.before_sleep_log(logger, logging.WARNING)
                )
def save_track(url, soundcloud_api):
    try:
        time.sleep(1)
        track = soundcloud_api.resolve(url)
        assert isinstance(track, Track), "URL is not managed to be a track"

        mp3_data = io.BytesIO()
        track.write_mp3_to(mp3_data)
        mp3_data.seek(0)

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            track.write_mp3_to(tmp_file)
            tmp_file.flush()
            temp_file_path = tmp_file.name

            track_artist_path = sanitizer.sanitize_path(track.artist)
            track_title_path = sanitizer.sanitize_path(track.title)
            supabase_path = f"{track_artist_path}_{track_title_path}.mp3"

        with open(temp_file_path, "rb") as mp3_file:
            mp3_data = mp3_file.read()

        track_bucket = "tracks"
        supabase.storage.from_(track_bucket).upload(
            path=supabase_path,
            file=mp3_data,
            file_options={"content-type": "audio/mp3"}
        )
        os.remove(temp_file_path)

        download_url = disk_to_db.get_url(track_bucket, supabase_path)
        track_id = disk_to_db.save_track_to_db(track.title, download_url)

        cover_path = f"{track_artist_path}_{track_title_path}.jpg"
        cover_path = sanitizer.sanitize_path(cover_path)
        cover_id = save_cover(track_id, track.artwork_url, cover_path)
        time.sleep(1)

        return track_id, cover_id



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


# сохранение альбома с sk в supabase
def save_album(url, soundcloud_api):
    """

    :param url:
    :param soundcloud_api:
    :type api: object
    """
    try:
        playlist = soundcloud_api.resolve(url)
        assert isinstance(playlist, Playlist), "URL is not managed to be a playlist"

        playlist_id = disk_to_db.save_playlist_to_db(playlist.title)
        track_ids = []
        album_bucket = "tracks"

        for track in playlist.tracks:
            time.sleep(1)

            @tenacity.retry(stop=tenacity.stop_after_attempt(5),
                            wait=tenacity.wait_fixed(3),
                            retry=tenacity.retry_if_exception_type(
                                (RequestException, StorageApiError, HTTPError, ConnectionResetError)),
                            before_sleep=tenacity.before_sleep_log(logger, logging.WARNING)
                            )
            def single_track():
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
                    track.write_mp3_to(tmp_file)
                    tmp_file.flush()
                    temp_file_path = tmp_file.name

                    playlist_title_path = sanitizer.sanitize_path(playlist.title)
                    track_artist_path = sanitizer.sanitize_path(track.artist)
                    track_title_path = sanitizer.sanitize_path(track.title)
                    supabase_path = f"{playlist_title_path}/{track_artist_path}_{track_title_path}.mp3"

                with open(temp_file_path, "rb") as mp3_file:
                    mp3_data = mp3_file.read()

                supabase.storage.from_(album_bucket).upload(
                    path=supabase_path,
                    file=mp3_data,
                    file_options={"content-type": "audio/mp3"}
                )
                os.remove(temp_file_path)

                solo_download_url = disk_to_db.get_url(album_bucket, supabase_path)

                solo_track_id = disk_to_db.save_track_to_db(track.title, solo_download_url, playlist_id)

                solo_cover_path = f"{playlist.title}/{track.artist}_{track.title}.jpg"
                solo_cover_path = sanitizer.sanitize_path(solo_cover_path)
                time.sleep(1)
                solo_cover_id = save_cover(solo_track_id, track.artwork_url, solo_cover_path)

                return solo_track_id, solo_cover_id

            track_id, _ = single_track()
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

    n = input(
        "Input what do you want to download? (1 - single track, 2 - album of  tracks, 3 - multiple of single tracks, 4 - multiple of albums):\n")
    match n:
        case '1':
            print("Single track")
            url = input("Input url: ")
            save_track(url, sc_api)
        case '2':
            print("Album of tracks")
            url = input("Input url: ")
            save_album(url, sc_api)
        case '3':
            print("Multiple tracks")
            num = int(input("Input number of tracks: "))
            urls = []

            for i in range(num):
                url = input(f"{i}: Input url: ")
                urls.append(url)

            for url in urls:
                save_track(url, sc_api)
        case '4':
            print("Multiple albums")
            num = int(input("Input number of albums: "))
            urls = []

            for i in range(num):
                url = input(f"{i}: Input url: ")
                urls.append(url)

            for url in urls:
                save_album(url, sc_api)
