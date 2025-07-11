from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.api.routes import tracks, playlists

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Femin tracks API (Refactored)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "https://femin-front.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tracks.router, prefix="/tracks", tags=["Tracks"])
app.include_router(playlists.router, prefix="/playlists", tags=["Playlists"])

@app.get("/")
def root():
    return {
        "message": "Welcome to Femin tracks API (Refactored)",
        "tracks": "/tracks",
        "playlists": "/playlists",
    } 