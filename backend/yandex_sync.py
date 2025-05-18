import io
import logging
import os
from urllib.error import HTTPError
import time
import requests
import tempfile
from requests import RequestException
from storage3.exceptions import StorageApiError
import config, disk_to_db, sanitizer
import tenacity
import supabase
from yandex_music import Client

logging.basicConfig(level=logging.INFO, format='%(asctime)s -- %(levelname)s -- %(message)s')
logger = logging.getLogger(__name__)

def extract_id_from_url(url):
    return url.split('/')[-1]

@tenacity.retry(stop=tenacity.stop_after_attempt(5),
                wait=tenacity.wait_fixed(3),
                retry=tenacity.retry_if_exception_type(
                    (RequestException, StorageApiError, HTTPError, ConnectionResetError)),
                before_sleep=tenacity.before_sleep_log(logger, logging.WARNING)
                )
def save_cover(track_id, artwork_url, cover_path):
    if not artwork_url:
        cover_id = config.DEFAULT_COVER
        return cover_id
    try:
        high_quality_cover = f'https://{artwork_url.replace("%%", "1000x1000")}'

        response = requests.get(high_quality_cover)

        response.raise_for_status()

        supabase.storage.from_("covers").upload(
            path=cover_path,
            file=response.content
        )
        public_url = supabase.storage.from_("covers").get_public_url(cover_path)
        cover_id = disk_to_db.save_cover_to_db(track_id, public_url)
        return cover_id
    except Exception as e:
        print(f"Error saving cover for track {track_id}: {e}")
        raise
    except StorageApiError as e:
        return


@tenacity.retry(stop=tenacity.stop_after_attempt(5),
                wait=tenacity.wait_fixed(3),
                retry=tenacity.retry_if_exception_type(
                    (RequestException, StorageApiError, HTTPError, ConnectionResetError)),
                before_sleep=tenacity.before_sleep_log(logger, logging.WARNING)
                )

def save_track(YaClient, track_id):
    try:
        track = YaClient.tracks([track_id])[0]

        # BYTES BRO WTF
        mp3_bytes = track.download_bytes()

        # PATH
        track_artist_path = '_'.join(sanitizer.sanitize_path(artist.name) for artist in track.artists)
        track_title_path = sanitizer.sanitize_path(track.title)
        supabase_path = f"{track_artist_path}_{track_title_path}.mp3"

        # supabase
        track_bucket = "tracks"
        supabase.storage.from_(track_bucket).upload(
            path=supabase_path,
            file=mp3_bytes,  # BYTES LOLLLL
            file_options={"content-type": "audio/mp3"}
        )

        download_url = disk_to_db.get_url(track_bucket, supabase_path)
        track_id = disk_to_db.save_track_to_db(track.title, download_url)

        # cover
        cover_path = f"{track_artist_path}_{track_title_path}.jpg"
        cover_path = sanitizer.sanitize_path(cover_path)
        cover_id = save_cover(track_id, track.cover_uri, cover_path)

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

@tenacity.retry(stop=tenacity.stop_after_attempt(5),
                wait=tenacity.wait_fixed(3),
                retry=tenacity.retry_if_exception_type(
                    (RequestException, StorageApiError, HTTPError, ConnectionResetError)),
                before_sleep=tenacity.before_sleep_log(logger, logging.WARNING)
                )
def save_album():
    pass
if __name__ == "__main__":
    supabase: Client = supabase.create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

    YandexClient = Client(config.YANDEX_TOKEN).init()
    url = input("Enter Yandex URL: ")
    id = extract_id_from_url(url)
    save_track(YandexClient, id)

