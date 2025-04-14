import io
import requests
import tempfile
from sclib import SoundcloudAPI, Track, Playlist
from PIL import Image
from datetime import datetime, timedelta
from backend.config import B2_KEY_ID, B2_APPLICATION_KEY, B2_BUCKET_NAME, default_cover
import b2sdk.v2 as b2
import psycopg2
from psycopg2.extras import DictCursor
from backend.disk_to_db import save_track_to_db, save_cover_to_db
##  инициализация бакета
def init_b2():
    info = b2.InMemoryAccountInfo()
    b2_api = b2.B2Api(info)
    b2_api.authorize_account('production', B2_KEY_ID, B2_APPLICATION_KEY)
    bucket = b2_api.get_bucket_by_name(B2_BUCKET_NAME)
    return b2_api, bucket


def get_url(b2_api, bucket, file_name, expires_in=3600):
    download_url = b2_api.get_download_url_for_file_name(bucket.bucket_name, file_name)
    signed_url = b2_api.get_download_authorization_token(bucket.bucket_name, file_name, expires_in=expires_in, prefix=None)

    full_url = f"{download_url}?Authorization={signed_url}"
    return full_url, expires_in

def generate_and_save_url(b2_api, bucket, path, table, url_column, expires_column, path_column, conn, cursor):
    signed_url, expires_in = get_url(b2_api, bucket, path)
    expires = datetime.now() + timedelta(seconds=expires_in)
    cursor.execute(
        f"UPDATE {table} SET {url_column} = %s, {expires_column} = %s WHERE {path_column} = %s", (signed_url, expires, path)
    )
    conn.commit()
    return signed_url

def refresh_url(b2_api, bucket, path, table, url_column, expires_column, path_column, conn, cursor, force=False):
    if not force:
        now = datetime.now()
        cursor.execute(
            f"SELECT {expires_column} FROM {table} WHERE {path_column} = %s", (path,)

        )
        result = cursor.fetchone()
        expires = result[0] if result else None
        if expires and expires > now:
            return path

    return generate_and_save_url(b2_api, bucket, path, table, url_column, expires_column, path_column, conn, cursor)


def update_url(b2_api, bucket, path, table, url_column, expires_column, path_column, conn, cursor):
    return refresh_url(b2_api, bucket, path, table, url_column, expires_column, path_column, conn, cursor, force=True)



def save_cover(track_id, cover_url, cover_path, bucket, conn, cursor):
    try:
        if not cover_url:
            cover_url = default_cover
        response = requests.get(cover_url or default_cover, timeout=10)
        bucket.upload_bytes(data_bytes=response.content, file_name=cover_path, content_type='image/jpeg')

        image = Image.open(io.BytesIO(response.content))
        resolution = f"{image.width}x{image.height}"
        file_size = image.size

        cover_signed_url, cover_expires_in = get_url(b2_api, bucket, cover_url)

        save_cover_to_db(track_id, cover_signed_url, resolution, file_size, cover_expires_in, conn, cursor)
        return True
    except Exception as e:
        print(e)
        return False



def save_track(url, b2_api, bucket, conn, cursor): # скачка трека - оперативка
    track = api.resolve(url)
    assert type(track) is Track

    mp3_data = io.BytesIO()
    track.write_mp3_to(mp3_data)
    mp3_data.seek(0)

    b2_path = f"/music/{track.artist} - {track.title}.mp3"
    bucket.upload_bytes(mp3_data.read(), b2_path, content_type='audio/mp3')
    mp3_data.close()

    signed_url, expires_in = get_url(b2_api, bucket, b2_path)
    track_id = save_track_to_db(track.title, signed_url, expires_in, conn, cursor)

    cover_path = f"music/covers/{track.artist} - {track.title}.jpg"
    save_cover(track_id, track.artwork_url, cover_path, bucket, conn, cursor)
    return track_id

def save_album(url, b2_api, bucket, conn, cursor):
    playlist = api.resolve(url)
    assert type(playlist) is Playlist

    track_ids = []
    playlist_path = f"music/{playlist.title}"

    for track in playlist.tracks:
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as f:
            track.write_mp3_to(f)

            b2_path = f"{playlist_path}/{track.artist} - {track.title}.mp3"
            bucket.upload_local_file(f.name, b2_path, content_type='audio/mp3')

            signed_url, expires_in = get_url(b2_api, bucket, b2_path)
            track_id = save_track_to_db(track.title, signed_url, expires_in, conn, cursor)
            track_ids.append(track_id)

            cover_path = f"music/covers/{playlist_path}/{track.artist} - {track.title}.jpg"
            save_cover(track.artwork_url, cover_path, bucket, conn, cursor)
    return track_ids

if __name__ == "__main__":
    b2_api, bucket = init_b2()
    api = SoundcloudAPI()
    # url = "https://soundcloud.com/illya-poludnenko/sets/serega-pirat"
    url = "https://soundcloud.com/user-544356536/sets/5uxxfdmldnek"
    save_album(url, b2_api, bucket)
