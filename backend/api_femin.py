import logging
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import DictCursor
from config import DB_NAME, DB_USER
from parsing_tracks_sync import init_b2

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
app = FastAPI(title="Femin tracks API")


class TrackResponse(BaseModel):
    title: str
    mp3_url: str
    cover_url: str


b2_api, bucket = init_b2()


def get_db():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, )
    try:
        yield conn
        # возвращает генератор который приостанавливает функцию
        # пока апи использует для запросов то есть необзятаельно закрывать
    finally:
        conn.close()


def get_signed_url(file_name: str) -> str:
    download_url = b2_api.get_download_url_for_file_name(bucket.name, file_name)
    return download_url


@app.get("/tracks", response_model=List[TrackResponse])
async def get_tracks(conn: psycopg2.extensions.connection = Depends(get_db)):
    try:
        cursor = conn.cursor(cursor_factory=DictCursor)
        cursor.execute("""
        SELECT t.track_id, t.title, t.file_path AS mp3_url, 
                c.image_path AS cover_url
        FROM tracks t
        LEFT JOIN covers c ON t.track_id = c.track_id
        """)
        tracks = cursor.fetchall()
        cursor.close()

        track_response = []
        for track in tracks:
            mp3_url = get_signed_url(track['mp3_url'])
            cover_url = get_signed_url(track['cover_url'])
            track_response.append(
                TrackResponse(
                    title=track["title"],
                    mp3_url=mp3_url,
                    cover_url=cover_url,
                )
            )
        logger.info(f"Got {len(track_response)} tracks")
        return track_response
    except Exception as e:
        logger.error(f"Got exception {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"message": "Welcome to Femin tracks API",
            "tracks": "http://localhost:8000/tracks"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
