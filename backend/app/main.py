from pathlib import Path

from fastapi import FastAPI
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
app.include_router(api_router)
app.mount(
    "/storage/audio",
    StaticFiles(directory=audio_storage_dir),
    name="audio-storage",
)
