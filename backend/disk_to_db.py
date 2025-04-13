# Правильный формат (Python + psycopg2)
import requests
import json
import pandas as pd
import psycopg2
import ssl
from sclib import SoundcloudAPI, Track, Playlist

api = SoundcloudAPI()
track = api.resolve('https://soundcloud.com/icegergert-685473693/casino')

assert type(track) is Track

filename = f'./{track.artist} - {track.title}.mp3'

with open(filename, 'wb+') as file:
    track.write_mp3_to(file)