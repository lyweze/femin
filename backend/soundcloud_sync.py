import io
import logging
import os
from typing import Optional, Tuple, List, Union
from urllib.error import HTTPError, URLError
import time
import requests
import tempfile
from requests import RequestException
from sclib import SoundcloudAPI, Track, Playlist
from storage3.exceptions import StorageApiError
import config, disk_to_db, sanitizer
import tenacity
from supabase import Client, create_client
from soundcloud_config import SOUNDCLOUD_CONFIG, URL_PATTERNS

logging.basicConfig(level=logging.INFO, format='%(asctime)s -- %(levelname)s -- %(message)s')
logger = logging.getLogger(__name__)

# Constants
COVER_BUCKET = SOUNDCLOUD_CONFIG['buckets']['covers']
TRACK_BUCKET = SOUNDCLOUD_CONFIG['buckets']['tracks']
DEFAULT_COVER_SIZE = SOUNDCLOUD_CONFIG['cover_size']
RETRY_ATTEMPTS = SOUNDCLOUD_CONFIG['retry_attempts']
RETRY_WAIT = SOUNDCLOUD_CONFIG['retry_wait']

def validate_soundcloud_url(url: str) -> str:
    """
    Validate if the provided URL is a valid SoundCloud URL.
    
    Args:
        url: URL to validate
        
    Returns:
        Validated URL
        
    Raises:
        ValueError: If URL is not a valid SoundCloud URL
    """
    url = url.strip()
    if not any(url.startswith(pattern) for pattern in URL_PATTERNS['soundcloud']):
        raise ValueError("Invalid SoundCloud URL. URL must start with https://soundcloud.com/")
    return url

def get_valid_url() -> str:
    """
    Get a valid SoundCloud URL from user input.
    
    Returns:
        Validated SoundCloud URL
    """
    while True:
        try:
            url = input("Enter URL: ").strip()
            return validate_soundcloud_url(url)
        except ValueError as e:
            print(f"Error: {e}. Please try again.")

def get_valid_number(prompt: str, min_val: int = 1) -> int:
    """
    Get a valid number from user input.
    
    Args:
        prompt: Input prompt message
        min_val: Minimum allowed value
        
    Returns:
        Validated number
    """
    while True:
        try:
            num = int(input(prompt))
            if num >= min_val:
                return num
            print(f"Please enter a number greater than or equal to {min_val}")
        except ValueError:
            print("Please enter a valid number")

@tenacity.retry(stop=tenacity.stop_after_attempt(RETRY_ATTEMPTS),
                wait=tenacity.wait_fixed(RETRY_WAIT),
                retry=tenacity.retry_if_exception_type(
                    (RequestException, StorageApiError, HTTPError, URLError, ConnectionResetError)),
                before_sleep=tenacity.before_sleep_log(logger, logging.WARNING)
                )
def save_cover(track_id: str, artwork_url: str, cover_path: str) -> str:
    """
    Save track cover to storage and database.
    
    Args:
        track_id: Track ID in database
        artwork_url: URL of the artwork from SoundCloud
        cover_path: Path where to save the cover in storage
        
    Returns:
        Cover ID from database if successful, default cover ID if no artwork
        
    Raises:
        RequestException: If download fails
        StorageApiError: If storage operations fail
    """
    if not artwork_url:
        logger.info(f"No artwork URL provided for track {track_id}, using default cover")
        return config.DEFAULT_COVER

    try:
        high_quality_url = artwork_url.replace("large", DEFAULT_COVER_SIZE)
        response = requests.get(high_quality_url)
        response.raise_for_status()

        supabase.storage.from_(COVER_BUCKET).upload(
            path=cover_path,
            file=response.content
        )
        public_url = supabase.storage.from_(COVER_BUCKET).get_public_url(cover_path)
        cover_id = disk_to_db.save_cover_to_db(track_id, public_url)
        return cover_id
    except Exception as e:
        logger.error(f"Error saving cover for track {track_id}: {e}")
        raise

@tenacity.retry(stop=tenacity.stop_after_attempt(RETRY_ATTEMPTS),
                wait=tenacity.wait_fixed(RETRY_WAIT),
                retry=tenacity.retry_if_exception_type(
                    (RequestException, StorageApiError, HTTPError, URLError, ConnectionResetError)),
                before_sleep=tenacity.before_sleep_log(logger, logging.WARNING)
                )
def save_track(url: str, soundcloud_api: SoundcloudAPI) -> Optional[Tuple[int, int]]:
    """
    Save a single track from SoundCloud to the database and storage.
    
    Args:
        url: SoundCloud track URL
        soundcloud_api: Initialized SoundCloud API client
        
    Returns:
        Tuple of (track_id, cover_id) if successful, None if failed
        
    Raises:
        AssertionError: If URL is not a valid track
        RequestException: If download fails
        StorageApiError: If storage operations fail
    """
    try:
        time.sleep(1)
        track = soundcloud_api.resolve(url)
        if not isinstance(track, Track):
            logger.error("URL is not a valid track")
            return None

        # Create a temporary file
        temp_file_path = tempfile.mktemp(suffix=".mp3")
        try:
            # Open file in wb+ mode for writing
            with open(temp_file_path, "wb+") as tmp_file:
                track.write_mp3_to(tmp_file)
                tmp_file.flush()

            track_artist_path = sanitizer.sanitize_path(track.artist)
            track_title_path = sanitizer.sanitize_path(track.title)
            supabase_path = f"{track_artist_path}_{track_title_path}.mp3"

            # Read the written MP3 data
            with open(temp_file_path, "rb") as mp3_file:
                mp3_data = mp3_file.read()

            supabase.storage.from_(TRACK_BUCKET).upload(
                path=supabase_path,
                file=mp3_data,
                file_options={"content-type": "audio/mp3"}
            )

            download_url = disk_to_db.get_url(TRACK_BUCKET, supabase_path)
            track_id = disk_to_db.save_track_to_db(track.title, download_url)

            cover_path = f"{track_artist_path}_{track_title_path}.jpg"
            cover_path = sanitizer.sanitize_path(cover_path)
            cover_id = save_cover(track_id, track.artwork_url, cover_path)
            time.sleep(1)

            return track_id, cover_id
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    except AssertionError as e:
        logger.error(f"Error: URL is not a track: {e}")
        return None
    except requests.RequestException as e:
        logger.error(f"Error: Network request failed: {e}")
        return None
    except StorageApiError as e:
        logger.error(f"Error: Storage operation failed: {e}")
        return None
    except URLError as e:
        logger.error(f"Error: Network connection failed: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None

def save_album(url: str, soundcloud_api: SoundcloudAPI) -> List[int]:
    """
    Save an album from SoundCloud to the database and storage.
    
    Args:
        url: SoundCloud album URL
        soundcloud_api: Initialized SoundCloud API client
        
    Returns:
        List of track IDs from the album
        
    Raises:
        AssertionError: If URL is not a valid album
        StorageApiError: If storage operations fail
        URLError: If network connection fails
    """
    try:
        playlist = soundcloud_api.resolve(url)
        if not isinstance(playlist, Playlist):
            logger.error("URL is not a valid playlist")
            return []

        playlist_id = disk_to_db.save_playlist_to_db(playlist.title)
        track_ids = []

        for track in playlist.tracks:
            time.sleep(1)

            @tenacity.retry(stop=tenacity.stop_after_attempt(RETRY_ATTEMPTS),
                            wait=tenacity.wait_fixed(RETRY_WAIT),
                            retry=tenacity.retry_if_exception_type(
                                (RequestException, StorageApiError, HTTPError, URLError, ConnectionResetError)),
                            before_sleep=tenacity.before_sleep_log(logger, logging.WARNING)
                            )
            def single_track() -> Tuple[int, int]:
                # Create a temporary file
                temp_file_path = tempfile.mktemp(suffix=".mp3")
                try:
                    # Open file in wb+ mode for writing
                    with open(temp_file_path, "wb+") as tmp_file:
                        track.write_mp3_to(tmp_file)
                        tmp_file.flush()

                    playlist_title_path = sanitizer.sanitize_path(playlist.title)
                    track_artist_path = sanitizer.sanitize_path(track.artist)
                    track_title_path = sanitizer.sanitize_path(track.title)
                    supabase_path = f"{playlist_title_path}/{track_artist_path}_{track_title_path}.mp3"

                    # Read the written MP3 data
                    with open(temp_file_path, "rb") as mp3_file:
                        mp3_data = mp3_file.read()

                    supabase.storage.from_(TRACK_BUCKET).upload(
                        path=supabase_path,
                        file=mp3_data,
                        file_options={"content-type": "audio/mp3"}
                    )

                    solo_download_url = disk_to_db.get_url(TRACK_BUCKET, supabase_path)
                    solo_track_id = disk_to_db.save_track_to_db(track.title, solo_download_url, playlist_id)

                    solo_cover_path = f"{playlist.title}/{track.artist}_{track.title}.jpg"
                    solo_cover_path = sanitizer.sanitize_path(solo_cover_path)
                    time.sleep(1)
                    solo_cover_id = save_cover(solo_track_id, track.artwork_url, solo_cover_path)

                    return solo_track_id, solo_cover_id
                finally:
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)

            track_id, _ = single_track()
            track_ids.append(track_id)

    except StorageApiError as e:
        logger.error(f"Error uploading the playlist: {e}")
        return []
    except URLError as e:
        logger.error(f"Error: Network connection failed: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return []

    return track_ids

def main():
    """Main function to handle user interaction and track/album downloads."""
    create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
    sc_api = SoundcloudAPI()

    print("\nSoundCloud Downloader")
    print("1 - Single track")
    print("2 - Album of tracks")
    print("3 - Multiple single tracks")
    print("4 - Multiple albums")
    
    choice = input("\nEnter your choice (1-4): ")
    
    try:
        match choice:
            case '1':
                url = get_valid_url()
                save_track(url, sc_api)
            case '2':
                url = get_valid_url()
                save_album(url, sc_api)
            case '3':
                num = get_valid_number("Enter number of tracks: ")
                urls = [get_valid_url() for _ in range(num)]
                for url in urls:
                    save_track(url, sc_api)
            case '4':
                num = get_valid_number("Enter number of albums: ")
                urls = [get_valid_url() for _ in range(num)]
                for url in urls:
                    save_album(url, sc_api)
            case _:
                print("Invalid choice. Please enter a number between 1 and 4.")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        print("An error occurred. Please check the logs for details.")

if __name__ == "__main__":
    main()
