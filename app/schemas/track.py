from pydantic import BaseModel

class TrackResponse(BaseModel):
    track_id: int
    title: str
    mp3_url: str
    cover_url: str 