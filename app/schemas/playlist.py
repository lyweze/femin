from pydantic import BaseModel

class PlaylistTrackResponse(BaseModel):
    playlist_id: int
    playlist_name: str
    track_id: int
    title: str
    mp3_url: str
    cover_url: str 