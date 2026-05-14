from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1.api import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging

configure_logging()
settings = get_settings()
audio_storage_dir = Path(__file__).resolve().parents[1] / "storage" / "audio"
audio_storage_dir.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)
app.mount(
    "/storage/audio",
    StaticFiles(directory=audio_storage_dir),
    name="audio-storage",
)
