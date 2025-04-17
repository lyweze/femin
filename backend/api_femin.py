import logging
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
app = FastAPI(title="Femin tracks API")


class TrackResponse(BaseModel):
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
        ).execute()
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

@app.get("/")
async def root():

    return {"message": "Welcome to Femin tracks API",
            "tracks": "http://localhost:8000/tracks"}


if __name__ == "__main__":
    supabase = get_supabase()
    uvicorn.run(app, host="0.0.0.0", port=8000)
