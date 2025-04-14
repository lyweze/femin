import io
import requests
import tempfile
from sclib import SoundcloudAPI, Track, Playlist

from backend.config import B2_KEY_ID, B2_APPLICATION_KEY, B2_BUCKET_NAME, default_cover
import b2sdk.v2 as b2

def init_b2():
    info = b2.InMemoryAccountInfo()
    b2_api = b2.B2Api(info)
    b2_api.authorize_account('production', B2_KEY_ID, B2_APPLICATION_KEY)
    bucket = b2_api.get_bucket_by_name(B2_BUCKET_NAME)
    return b2_api, bucket

def save_cover(cover_url, b2_path, bucket):

    try:
        if not cover_url:
            cover_url = default_cover

        response = requests.get(cover_url)
        bucket.upload_bytes(data_bytes=response.content, file_name=b2_path, content_type='image/jpeg')
        return True
    except Exception as e:
        print(e)
        return False

def save_track(url, b2_api, bucket): # скачка трека - оперативка
    track = api.resolve(url)
    assert type(track) is Track

    mp3_data = io.BytesIO()
    track.write_mp3_to(mp3_data)
    mp3_data.seek(0)

    b2_path = f"/music/{track.artist} - {track.title}.mp3"
    bucket.upload_bytes(mp3_data.read(), b2_path, content_type='audio/mp3')
    mp3_data.close()

    cover_path = f"music/covers/{track.artist} - {track.title}.jpg"
    save_cover(track.artwork_url, cover_path, bucket)
    return 1

def save_album(url, b2_api, bucket):
    playlist = api.resolve(url)
    assert type(playlist) is Playlist

    playlist_path = f"music/{playlist.title}"

    for track in playlist.tracks:
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as f:
            track.write_mp3_to(f)

            b2_path = f"{playlist_path}/{track.artist} - {track.title}.mp3"
            bucket.upload_local_file(f.name, b2_path, content_type='audio/mp3')

            cover_path = f"music/covers/{track.artist} - {track.title}.jpg"
            save_cover(track.artwork_url, cover_path, bucket)
    return 1

if __name__ == "__main__":
    b2_api, bucket = init_b2()
    api = SoundcloudAPI()
    # url = "https://soundcloud.com/illya-poludnenko/sets/serega-pirat"
    url = "https://soundcloud.com/user-544356536/sets/5uxxfdmldnek"
    save_album(url, b2_api, bucket)
