import io
import logging
import os
from typing import Optional, Tuple, List, Union
from urllib.error import HTTPError
import time
import requests
import tempfile
from requests import RequestException
from storage3.exceptions import StorageApiError
import config, disk_to_db, sanitizer
import tenacity
import supabase

from savify import Savify
from savify.types import Type, Format, Quality

s = Savify()
# Spotify URL
url = 'https://open.spotify.com/track/3QFInJAm9eyaho5vBzxInN'
s.download(url)

# Search Query
# Types: TRACK, ALBUM, PLAYLIST
s.download("QUERY", query_type=Type.TRACK)