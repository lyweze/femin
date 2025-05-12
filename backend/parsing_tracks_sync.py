import io
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Tuple, Union
from urllib.error import HTTPError
import time
import requests
import tempfile
from requests import RequestException
from sclib import SoundcloudAPI, Track, Playlist
from storage3.exceptions import StorageApiError
import config
import disk_to_db
import tenacity
from supabase import Client, create_client

logging.basicConfig(level=logging.INFO, format='%(asctime)s -- %(levelname)s -- %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class TrackResult:
    track_id: str
    cover_id: str


class SoundCloudManager:
    def __init__(self, supabase_client: Client, soundcloud_api: SoundcloudAPI):
        self.supabase = supabase_client
        self.sc_api = soundcloud_api
        self._transliteration = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
            'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
            'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
            'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
            'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
        }

    def _sanitize_path(self, text: str) -> str:
        """Sanitize text for use in file paths."""
        text = text.lower()
        return ''.join(self._transliteration.get(c, c) for c in text)

    def _get_public_url(self, bucket_name: str, file_path: str) -> str:
        """Get public URL for a file in storage."""
        return self.supabase.storage.from_(bucket_name).get_public_url(file_path)

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(5),
        wait=tenacity.wait_fixed(3),
        retry=tenacity.retry_if_exception_type((RequestException, StorageApiError, HTTPError)),
        before_sleep=tenacity.before_sleep_log(logger, logging.WARNING)
    )
    def _save_cover(self, track_id: str, artwork_url: str, cover_path: str) -> str:
        """Save track cover to storage."""
        if not artwork_url:
            return config.DEFAULT_COVER

        try:
            high_quality_url = artwork_url.replace("large", "t500x500")
            response = requests.get(high_quality_url, timeout=10)
            response.raise_for_status()

            self.supabase.storage.from_("covers").upload(
                path=cover_path,
                file=response.content
            )
            public_url = self._get_public_url("covers", cover_path)
            return disk_to_db.save_cover_to_db(track_id, public_url)
        except Exception as e:
            logger.error(f"Error saving cover for track {track_id}: {e}")
            raise

    def _save_track_file(self, track: Track, file_path: str) -> str:
        """Save track audio file to storage."""
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as tmp_file:
            track.write_mp3_to(tmp_file)
            tmp_file.flush()
            
            with open(tmp_file.name, "rb") as mp3_file:
                self.supabase.storage.from_("tracks").upload(
                    path=file_path,
                    file=mp3_file.read(),
                    file_options={"content-type": "audio/mp3"}
                )

        return self._get_public_url("tracks", file_path)

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(5),
        wait=tenacity.wait_fixed(3),
        retry=tenacity.retry_if_exception_type((RequestException, StorageApiError, HTTPError)),
        before_sleep=tenacity.before_sleep_log(logger, logging.WARNING)
    )
    def save_track(self, url: str) -> Optional[TrackResult]:
        """Save a single track from SoundCloud."""
        try:
            track = self.sc_api.resolve(url)
            if not isinstance(track, Track):
                logger.error(f"URL is not a track: {url}")
                return None

            track_path = f"{self._sanitize_path(track.artist)}_{self._sanitize_path(track.title)}.mp3"
            download_url = self._save_track_file(track, track_path)
            track_id = disk_to_db.save_track_to_db(track.title, download_url)

            cover_path = f"{self._sanitize_path(track.artist)}_{self._sanitize_path(track.title)}.jpg"
            cover_id = self._save_cover(track_id, track.artwork_url, cover_path)

            return TrackResult(track_id=track_id, cover_id=cover_id)

        except Exception as e:
            logger.error(f"Failed to save track {url}: {e}")
            return None

    def save_album(self, url: str) -> List[str]:
        """Save an album/playlist from SoundCloud."""
        try:
            playlist = self.sc_api.resolve(url)
            if not isinstance(playlist, Playlist):
                logger.error(f"URL is not a playlist: {url}")
                return []

            playlist_id = disk_to_db.save_playlist_to_db(playlist.title)
            track_ids = []
            playlist_path = self._sanitize_path(playlist.title)

            for track in playlist.tracks:
                track_path = f"{playlist_path}/{self._sanitize_path(track.artist)}_{self._sanitize_path(track.title)}.mp3"
                download_url = self._save_track_file(track, track_path)
                track_id = disk_to_db.save_track_to_db(track.title, download_url, playlist_id)
                
                cover_path = f"{playlist_path}/{self._sanitize_path(track.artist)}_{self._sanitize_path(track.title)}.jpg"
                self._save_cover(track_id, track.artwork_url, cover_path)
                
                track_ids.append(track_id)

            return track_ids

        except Exception as e:
            logger.error(f"Failed to save album {url}: {e}")
            return []


def main():
    supabase = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
    sc_api = SoundcloudAPI()
    manager = SoundCloudManager(supabase, sc_api)

    options = {
        '1': ('Single track', lambda: manager.save_track(input("Input url: "))),
        '2': ('Album of tracks', lambda: manager.save_album(input("Input url: "))),
        '3': ('Multiple tracks', lambda: [manager.save_track(input(f"{i}: Input url: ")) 
                                        for i in range(int(input("Input number of tracks: ")))]),
        '4': ('Multiple albums', lambda: [manager.save_album(input(f"{i}: Input url: ")) 
                                        for i in range(int(input("Input number of albums: ")))])
    }

    choice = input(
        "Input what do you want to download?\n"
        "1 - single track\n"
        "2 - album of tracks\n"
        "3 - multiple single tracks\n"
        "4 - multiple albums\n"
    )

    if choice in options:
        print(options[choice][0])
        options[choice][1]()
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
