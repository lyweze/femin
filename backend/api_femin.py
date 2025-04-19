import logging
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from supabase import create_client, Client
from backend.config import SUPABASE_URL, SUPABASE_KEY
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
app = FastAPI(title="Femin tracks API")


class TrackResponse(BaseModel):
    track_id: int
    title: str
    mp3_url: str
    cover_url: str

class PlaylistTrackResponse(BaseModel):
    playlist_id: int
    playlist_name: str
    track_id: int
    title: str
    mp3_url: str
    cover_url: str

def get_supabase() -> Client:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return supabase




@app.get("/tracks", response_model=List[TrackResponse])
async def get_tracks(supabase: Client = Depends(get_supabase)):
    try:
        response = supabase.table("tracks").select(
            'track_id',
            'title',
            'file_path',
            'covers(image_path)',
        ).is_("playlist_id", None).execute()
        tracks = response.data
        track_response = []
        for track in tracks:
            cover_url = track['covers'][0]['image_path'] if track['covers'] else ""
            track_response.append(TrackResponse(
                track_id=track['track_id'],
                title=track['title'],
                mp3_url=track['file_path'],
                cover_url=cover_url,
            ))
        logger.info(f"Got {len(track_response)} tracks")
        return track_response
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Something went wrong")

@app.get("/playlists", response_model=List[PlaylistTrackResponse])
async def get_playlists(supabase: Client = Depends(get_supabase)):
    try:
        response = supabase.table("tracks").select(
            'playlist_id',
            'playlists(title)',
            'track_id',
            'title',
            'file_path',
            'covers(image_path)',
        ).not_.is_("playlist_id", None).execute()

        tracks = response.data
        playlist_response = []

        for track in tracks:
            cover_url = track['covers'][0]['image_path'] if track['covers'] else ""
            playlist_name = track['playlists']['title'] if track['playlists'] else "Unknown Playlist"
            playlist_response.append(PlaylistTrackResponse(
                playlist_id=track['playlist_id'],
                playlist_name = playlist_name,
                track_id=track['track_id'],
                title=track['title'],
                mp3_url=track['file_path'],
                cover_url=cover_url
            ))
        logger.info(f"Got {len(playlist_response)} playlists")
        return playlist_response
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Something went wrong")
@app.get("/")
async def root():

    return {"message": "Welcome to Femin tracks API",
            "tracks": "femin.onrender.com/tracks",
            "playlists": "femin.onrender.com/playlists"}


if __name__ == "__main__":
    supabase = get_supabase()
    uvicorn.run(app, host="0.0.0.0", port=8000)
