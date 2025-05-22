from savify import Savify
from savify.types import Type

s = Savify()
# Spotify URL
url = 'https://open.spotify.com/track/3QFInJAm9eyaho5vBzxInN'
s.download(url)

# Search Query
# Types: TRACK, ALBUM, PLAYLIST
s.download("QUERY", query_type=Type.TRACK)