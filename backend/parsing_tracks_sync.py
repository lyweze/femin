import io
import logging
import os
import psycopg2
import requests
import tempfile
from psycopg2.extras import DictCursor
from requests import RequestException
from sclib import SoundcloudAPI, Track, Playlist
from PIL import Image
from datetime import datetime, timedelta
from backend.config import B2_KEY_ID, B2_APPLICATION_KEY, B2_BUCKET_NAME, default_cover, DB_NAME, DB_USER
import b2sdk.v2 as b2
from disk_to_db import save_track_to_db
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type, before_sleep_log
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s -- %(levelname)s -- %(message)s')
logger = logging.getLogger(__name__)

def init_db():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER)
    return conn
##  инициализация бакета
def init_b2():
    info = b2.InMemoryAccountInfo()
    b2_api = b2.B2Api(info)
    b2_api.authorize_account('production', B2_KEY_ID, B2_APPLICATION_KEY)
    bucket = b2_api.get_bucket_by_name(B2_BUCKET_NAME)
    return b2_api, bucket

## получаем ссылку на backblaze
def get_url(bucket, file_name):
    download_url = b2_api.get_download_url_for_file_name(bucket.name, file_name)
    print(f"Generating URL for bucket: {bucket.name}, file: {file_name}")
    expires_in = 1
    return download_url, expires_in

## сохранение обложки
@retry(stop=stop_after_attempt(5),
       wait=wait_fixed(3),
       retry=retry_if_exception_type((RequestException, Exception)),
        before_sleep=before_sleep_log(logger, logging.WARNING)
       )
def save_cover(track_id, cover_url, cover_path, bucket, conn, cursor):
    try:
        if not cover_url:
            cover_url = default_cover

        response = requests.get(cover_url, timeout=10)
        response.raise_for_status()


        bucket.upload_bytes(data_bytes=response.content, file_name=cover_path, content_type='image/jpeg')

        image = Image.open(io.BytesIO(response.content))
        resolution = f"{image.width}x{image.height}"
        file_size = len(response.content) // 1024

        cursor.execute(
            "SELECT cover_id, url_expires FROM covers WHERE image_path = %s", (cover_path,)
        )
        result = cursor.fetchone()
        now = datetime.now()

        if result:

            cover_id, url_expires = result
            if url_expires and url_expires <= now:

                signed_url, expires_in = get_url(bucket, cover_path)
                expires_time = datetime.now() + timedelta(hours=expires_in)
                cursor.execute(
                    "UPDATE covers SET image_path = %s, url_expires = %s WHERE cover_id = %s",
                    (signed_url, expires_time, cover_id)
                )
                conn.commit()
            return cover_id
        else:
            signed_url, expires_in = get_url(bucket, cover_path)
            expires_time = datetime.now() + timedelta(hours=expires_in)
            cursor.execute(
                """
                INSERT INTO covers (track_id, image_path, resolution, file_size, url_expires)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING cover_id
                """,
                (track_id, signed_url, resolution, file_size, expires_time)
            )
            cover_id = cursor.fetchone()[0]
            conn.commit()
            return cover_id

    except requests.RequestException as e:
        print(f"error by trying ti get the cover: {e}")
        return None
    except Exception as e:
        print(f"error by uploading the cover: {e}")
        return None

# сохранение трека в backblaze
@retry(stop=stop_after_attempt(5),
       wait=wait_fixed(3),
       retry=retry_if_exception_type((RequestException, Exception)),
        before_sleep=before_sleep_log(logger, logging.WARNING)
       )
def save_track(url, bucket, conn, cursor):
    try:
        time.sleep(1)
        track = api.resolve(url)
        assert isinstance(track, Track), "URL is not managed to be a playlist"

        mp3_data = io.BytesIO()
        track.write_mp3_to(mp3_data)
        mp3_data.seek(0)

        b2_path = f"music/{track.artist} - {track.title}.mp3"
        bucket.upload_bytes(mp3_data.read(), b2_path, content_type='audio/mp3')
        mp3_data.close()

        signed_url, expires_in = get_url(bucket, b2_path)

        track_id = save_track_to_db(track.title, signed_url, expires_in, conn, cursor)

        cover_path = f"music/covers/{track.artist} - {track.title}.jpg"
        cover_id = save_cover(track_id, track.artwork_url, cover_path, bucket, conn, cursor)
        if cover_id is None:
            print("Cover is not saved")

        return track_id

    except AssertionError as e:
        print(f"Error: url isnt a track: {e}")
        return None
    except requests.RequestException as e:
        print(f"Error: url isn't a track: {e}")
        return None
    except Exception as e:
        print(f"eRROR WE CANT MANAGED THIS TRACK: {e}")
        return None
# сохранение альбома в baclblazr

def save_album(url, bucket, conn, cursor):
    try:
        playlist = api.resolve(url)
        assert isinstance(playlist, Playlist), "URL is not managed to be a playlist"

        track_ids = []
        playlist_path = f"music/{playlist.title}"

        for track in playlist.tracks:
            time.sleep(1)

            @retry(stop=stop_after_attempt(5),
                       wait=wait_fixed(3),
                   retry=retry_if_exception_type((RequestException, Exception)),
                       before_sleep=before_sleep_log(logger, logging.WARNING)
                    )
            def single_track():
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                    track.write_mp3_to(f)
                    f.flush()
                    b2_path = f"music/{playlist_path}/{track.artist} - {track.title}.mp3"
                    bucket.upload_local_file(f.name, b2_path, content_type='audio/mp3')
                    os.remove(f.name)

                    signed_url, expires_in = get_url(bucket, b2_path)

                    track_id = save_track_to_db(track.title, signed_url, expires_in, conn, cursor)
                    track_ids.append(track_id)

                    cover_path = f"music/covers/{playlist_path}/{track.artist} - {track.title}.jpg"
                    time.sleep(1)

                    cover_id =save_cover(track_id, track.artwork_url, cover_path, bucket, conn, cursor)
                    return track_id, cover_id
            try:
                track_id, cover_id = single_track()
                track_ids.append(track_id)

            except Exception as e:
                logging.error(f"error by uploading the cover: {e}")
                continue
        return track_ids
    except AssertionError as e:
        logging.error(f"error by uploading the track, its not id: {e}")
        return []
    except Exception as e:
        logging.error(f"error by uploading the playlist: {e}")
        return []


if __name__ == "__main__":
    b2_api, bucket = init_b2()
    api = SoundcloudAPI()
    #url = "https://soundcloud.com/muc-sik/uglystephan-milly-rock-x-slime-love-speed-up"
    url = "https://soundcloud.com/pershin-maksim/sets/dsrfsfs"

    urls = ["https://soundcloud.com/elizaveta-lavrova-108256826/sets/morgenshtern-golden-edition",
            "https://soundcloud.com/instasamka/sets/moneydealer"]
    conn = init_db()
    cursor = conn.cursor(cursor_factory=DictCursor)
    for url in urls:
        logging.info(f"Starting playlist: {url}")
        conn = init_db()
        cursor = conn.cursor(cursor_factory=DictCursor)
        try:
            track_ids = save_album(url, bucket, conn, cursor)
            if track_ids:
                logging.info(f"Saved {len(track_ids)} tracks for {url}")
            else:
                logging.warning(f"No tracks saved for {url}")
        except Exception as e:
            logging.error(f"Failed to process {url}: {e}")
        finally:
            cursor.close()
            conn.close()
    '''try:
        track_id = save_track(url, bucket, conn, cursor)
        if track_id:
            print(f"Track saved successfully with ID: {track_id}")
        else:
            print("How no guts to save this track?")
    finally:
        cursor.close()
        conn.close()'''