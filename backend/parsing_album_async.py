import asyncio
from tqdm.asyncio import tqdm_asyncio
from sclib.asyncio import SoundcloudAPI, Playlist
import yadisk
from cfg.config import TOKEN_YA


async def save_track(cover_url) -> bool:
    try:
        if not cover_url:
            pass
    except:
        pass


async def save_album(url: str, y: yadisk.YaDisk) -> int:
    api = SoundcloudAPI()

    playlist = await api.resolve(url)
    assert isinstance(playlist, Playlist), "URL must be a playlist"

    playlist_path = f"music/{playlist.title}"
    if not y.exists(playlist_path):
        y.mkdir(playlist_path)

    async def upload_track(track):
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as f:
            await track.write_mp3_to(f)
            disk_path = f"{playlist_path}/{track.artist} - {track.title}.mp3"
            y.upload(f.name, disk_path)

    tasks = [upload_track(track) for track in playlist.tracks]
    await tqdm_asyncio.gather(*tasks, desc=f"Uploading {playlist.title}")

    return 1


async def main():
    y = yadisk.YaDisk(token=TOKEN_YA)
    # url = "https://soundcloud.com/icegergert-685473693/casino"
    url = "https://soundcloud.com/illya-poludnenko/sets/serega-pirat"
    await save_album(url, y)


if __name__ == "__main__":
    asyncio.run(main())
