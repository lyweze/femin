import asyncio
import io
from tqdm.asyncio import tqdm_asyncio
import tempfile
from sclib import SoundcloudAPI, Track, Playlist
from sclib.asyncio import SoundcloudAPI, Playlist
import yadisk
from config import tok

def save_track(url): # скачка трека - оперативка
    track = api.resolve(url)
    assert type(track) is Track

    mp3_data = io.BytesIO()
    track.write_mp3_to(mp3_data)
    mp3_data.seek(0)

    disk_path = f"/music/{track.artist} - {track.title}.mp3"
    y.upload(mp3_data, disk_path)

    mp3_data.close()
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
    return 1

if __name__ == "__main__":
    y = yadisk.YaDisk(token=tok)
    api = SoundcloudAPI()
    url = "https://soundcloud.com/illya-poludnenko/sets/serega-pirat"
    save_track(url)
