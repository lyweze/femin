import os

import logging
from typing import Optional, Tuple, Union
from urllib.error import HTTPError
import requests
from requests import RequestException
from storage3.exceptions import StorageApiError
import disk_to_db
import sanitizer
import tenacity
import supabase
from yandex_music import Client
from services.yandex.yandex_config import YANDEX_CONFIG, ERROR_MESSAGES
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s -- %(levelname)s -- %(message)s"
)
logger = logging.getLogger(__name__)

YANDEX_TOKEN = os.getenv("YANDEX_TOKEN")
DEFAULT_COVER = os.getenv("DEFAULT_COVER")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
COVER_BUCKET = YANDEX_CONFIG["buckets"]["covers"]
TRACK_BUCKET = YANDEX_CONFIG["buckets"]["tracks"]
DEFAULT_COVER_SIZE = YANDEX_CONFIG["cover_size"]
RETRY_ATTEMPTS = YANDEX_CONFIG["retry_attempts"]
RETRY_WAIT = YANDEX_CONFIG["retry_wait"]
MP3_OPTIONS = YANDEX_CONFIG["file_options"]["mp3"]


def extract_id_from_url(yandex_url: str) -> int:
    """
    Extract track/album ID from Yandex Music URL.

    Args:
        yandex_url: Yandex Music URL to extract ID from

    Returns:
        Extracted ID as integer

    Raises:
        ValueError: If URL is empty or invalid
    """
    if not yandex_url:
        raise ValueError(ERROR_MESSAGES["empty_url"])
    return int(yandex_url.split("/")[-1])


@tenacity.retry(
    stop=tenacity.stop_after_attempt(RETRY_ATTEMPTS),
    wait=tenacity.wait_fixed(RETRY_WAIT),
    retry=tenacity.retry_if_exception_type(
        (RequestException, StorageApiError, HTTPError, ConnectionResetError)
    ),
    before_sleep=tenacity.before_sleep_log(logger, logging.WARNING),
)
def save_cover(
    track_id: int, artwork_url: str, cover_path: str
) -> Optional[Union[str, int]]:
    """
    Save track cover to storage and database.

    Args:
        track_id: Track ID in database
        artwork_url: URL of the artwork from Yandex Music
        cover_path: Path where to save the cover in storage

    Returns:
        Cover ID from database if successful, None if failed

    Raises:
        RequestException: If download fails
        StorageApiError: If storage operations fail
        HTTPError: If artwork URL is invalid
    """
    if not artwork_url:
        cover_id = DEFAULT_COVER
        return cover_id
    try:
        high_quality_cover = f"https://{artwork_url.replace('%%', DEFAULT_COVER_SIZE)}"

        response_cover = requests.get(high_quality_cover)
        response_cover.raise_for_status()

        supabase.storage.from_(COVER_BUCKET).upload(
            path=cover_path, file=response_cover.content
        )
        public_url = supabase.storage.from_(COVER_BUCKET).get_public_url(cover_path)
        cover_id = disk_to_db.save_cover_to_db(track_id, public_url)
        return cover_id
    except Exception as e:
        logger.error(
            f"{ERROR_MESSAGES['cover_download_failed']} for track {track_id}: {e}"
        )
        raise
    except StorageApiError:
        logger.error(f"{ERROR_MESSAGES['cover_upload_failed']} for track {track_id}")
        return None


@tenacity.retry(
    stop=tenacity.stop_after_attempt(RETRY_ATTEMPTS),
    wait=tenacity.wait_fixed(RETRY_WAIT),
    retry=tenacity.retry_if_exception_type(
        (RequestException, StorageApiError, HTTPError, ConnectionResetError)
    ),
    before_sleep=tenacity.before_sleep_log(logger, logging.WARNING),
)
def save_track(YaClient: Client, track_id: int) -> Optional[Tuple[int, Optional[int]]]:
    """
    Save a single track from Yandex Music to the database and storage.

    Args:
        YaClient: Initialized Yandex Music API client
        track_id: Track ID from Yandex Music

    Returns:
        Tuple of (track_id, cover_id) if successful, None if failed

    Raises:
        AssertionError: If track_id is not a valid track
        RequestException: If download fails
        StorageApiError: If storage operations fail
        HTTPError: If track URL is invalid
    """
    try:
        track = YaClient.tracks([track_id])[0]

        # BYTES BRO WTF
        mp3_bytes = track.download_bytes()

        # PATH
        track_artist_path = "_".join(
            sanitizer.sanitize_path(artist.name) for artist in track.artists
        )
        track_title_path = sanitizer.sanitize_path(track.title)
        supabase_path = f"{track_artist_path}_{track_title_path}.mp3"

        # supabase
        supabase.storage.from_(TRACK_BUCKET).upload(
            path=supabase_path, file=mp3_bytes, file_options=MP3_OPTIONS
        )

        download_url = disk_to_db.get_url(TRACK_BUCKET, supabase_path)
        track_id = disk_to_db.save_track_to_db(track.title, download_url)

        # cover
        cover_path = f"{track_artist_path}_{track_title_path}.jpg"
        cover_path = sanitizer.sanitize_path(cover_path)
        cover_id = save_cover(track_id, track.cover_uri, cover_path)

        return track_id, cover_id

    except AssertionError as e:
        logger.error(f"{ERROR_MESSAGES['track_not_found']}: {e}")
        return None
    except requests.RequestException as e:
        logger.error(f"{ERROR_MESSAGES['download_failed']}: {e}")
        return None
    except StorageApiError as e:
        logger.error(f"{ERROR_MESSAGES['upload_failed']}: {e}")
        return None
    except HTTPError as e:
        logger.error(f"{ERROR_MESSAGES['download_failed']}: {e}")
        return None


@tenacity.retry(
    stop=tenacity.stop_after_attempt(RETRY_ATTEMPTS),
    wait=tenacity.wait_fixed(RETRY_WAIT),
    retry=tenacity.retry_if_exception_type(
        (RequestException, StorageApiError, HTTPError, ConnectionResetError)
    ),
    before_sleep=tenacity.before_sleep_log(logger, logging.WARNING),
)
def save_album() -> None:
    """
    Save an album from Yandex Music to the database and storage.

    This function is currently not implemented.

    Returns:
        None

    Raises:
        NotImplementedError: This function is not yet implemented
    """
    pass


if __name__ == "__main__":
    supabase: Client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

    YandexClient = Client(YANDEX_TOKEN).init()
    url = input("Enter Yandex URL: ")
    id_track = extract_id_from_url(url)
    save_track(YandexClient, id_track)
