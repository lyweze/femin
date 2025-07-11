from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.api.dependencies.db import get_supabase
from app.schemas.track import TrackResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/", response_model=List[TrackResponse])
async def get_tracks(supabase = Depends(get_supabase)):
    try:
        response = (
            supabase.table("tracks")
            .select("track_id", "title", "file_path", "covers(image_path)")
            .is_("playlist_id", None)
            .execute()
        )
        tracks = response.data
        track_response = []
        for track in tracks:
            cover_url = track["covers"][0]["image_path"] if track["covers"] else ""
            track_response.append(
                TrackResponse(
                    track_id=track["track_id"],
                    title=track["title"],
                    mp3_url=track["file_path"],
                    cover_url=cover_url,
                )
            )
        logger.info(f"Got {len(track_response)} tracks")
        return track_response
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Something went wrong") 