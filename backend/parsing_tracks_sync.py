import io
import requests
import tempfile
from sclib import SoundcloudAPI, Track, Playlist
import yadisk
from config import tok, default_cover


def save_cover(cover_url, save_to):

    try:
        if not cover_url:
            cover_url = default_cover

        response = requests.get(cover_url)
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=True) as f:
            f.write(response.content)
            f.flush()
            y.upload(f.name, save_to)
    except Exception as e:
        print(e)
        return False

def save_track(url): # скачка трека - оперативка
    track = api.resolve(url)
    assert type(track) is Track

    mp3_data = io.BytesIO()
    track.write_mp3_to(mp3_data)
    mp3_data.seek(0)

    disk_path = f"/music/{track.artist} - {track.title}.mp3"
    y.upload(mp3_data, disk_path)
    mp3_data.close()

    cover_path = f"music/covers/{track.artist} - {track.title}.jpg"
    save_cover(track.artwork_url, cover_path)
    return 1

def save_album(url):
    playlist = api.resolve(url)
    assert type(playlist) is Playlist

    playlist_path = f"music/{playlist.title}"
    if not y.exists(playlist_path):
        y.mkdir(playlist_path)
    for track in playlist.tracks:
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as f:
            track.write_mp3_to(f)

            disk_path = f"{playlist_path}/{track.artist} - {track.title}.mp3"
            y.upload(f.name, disk_path)

            cover_path = f"music/covers/{track.artist} - {track.title}.jpg"
            save_cover(track.artwork_url, cover_path)
    return 1

if __name__ == "__main__":
    y = yadisk.YaDisk(token=tok)
    api = SoundcloudAPI()
    # url = "https://soundcloud.com/illya-poludnenko/sets/serega-pirat"
    url = "https://soundcloud.com/user-544356536/sets/5uxxfdmldnek"
    save_album(url)
