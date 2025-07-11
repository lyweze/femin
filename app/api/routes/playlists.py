from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.api.dependencies.db import get_supabase
from app.schemas.playlist import PlaylistTrackResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/", response_model=List[PlaylistTrackResponse])
async def get_playlists(supabase = Depends(get_supabase)):
    try:
        response = (
            supabase.table("tracks")
            .select("playlist_id", "playlists(title)", "track_id", "title", "file_path", "covers(image_path)")
            .not_.is_("playlist_id", None)
            .execute()
        )
        tracks = response.data
        playlist_response = []
        for track in tracks:
            cover_url = track["covers"][0]["image_path"] if track["covers"] else ""
            playlist_name = track["playlists"]["title"] if track["playlists"] else "Unknown Playlist"
            playlist_response.append(
                PlaylistTrackResponse(
                    playlist_id=track["playlist_id"],
                    playlist_name=playlist_name,
                    track_id=track["track_id"],
                    title=track["title"],
                    mp3_url=track["file_path"],
                    cover_url=cover_url,
                )
            )
        logger.info(f"Got {len(playlist_response)} playlists")
        return playlist_response
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Something went wrong") 