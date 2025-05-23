from savify import Savify
from savify.types import Type
from savify.utils import PathHolder
from cfg.config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('savify')

# Set proxy environment variables
os.environ['http_proxy'] = 'socks5://78.63.115.20:8899'  # Замените на ваш прокси
os.environ['https_proxy'] = 'socks5://78.63.115.20:8899'  # Замените на ваш прокси

# Create download directory if it doesn't exist
download_dir = os.path.join(os.path.dirname(__file__), 'downloads')
os.makedirs(download_dir, exist_ok=True)

# Initialize Savify with proper configuration
s = Savify(
    api_credentials=(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET),
    path_holder=PathHolder(downloads_path=download_dir),
    logger=logger
)

# Spotify URL
url = 'https://open.spotify.com/track/3QFInJAm9eyaho5vBzxInN'
s.download(url)

# Search Query
# Types: TRACK, ALBUM, PLAYLIST
s.download("QUERY", query_type=Type.TRACK)