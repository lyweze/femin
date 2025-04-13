import yadisk
import asyncio
from config import tok

y = yadisk.YaDisk(token=tok)
from sclib import SoundcloudAPI, Track, Playlist

api = SoundcloudAPI()
track = api.resolve('https://soundcloud.com/icegergert-685473693/casino')

assert type(track) is Track

filename = f'./{track.artist} - {track.title}.mp3'

with open(filename, 'wb+') as file:
    track.write_mp3_to(file)

# y.upload("file1.txt", "/music/file1.txt")
# Правильный формат (Python + psycopg2)