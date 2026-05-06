from pathlib import Path

from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import app
from app.services import tts_service


def test_text_to_speech_returns_audio_url_and_mock_file_without_openai_key(
    monkeypatch,
) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    get_settings.cache_clear()

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/text-to-speech",
            json={"text": "Hello! Let's talk about animals today."},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["audio_url"].startswith("/storage/audio/")
    assert body["audio_url"].endswith(".mp3")

    audio_path = Path(tts_service.AUDIO_STORAGE_DIR) / Path(body["audio_url"]).name
    assert audio_path.exists()
    assert audio_path.read_bytes() == tts_service.MOCK_MP3_BYTES
    get_settings.cache_clear()


def test_text_to_speech_static_audio_url_is_browser_accessible(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    get_settings.cache_clear()

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/text-to-speech",
            json={"text": "Hello!"},
        )
        audio_response = client.get(response.json()["audio_url"])

    assert audio_response.status_code == 200
    assert audio_response.content == tts_service.MOCK_MP3_BYTES
    get_settings.cache_clear()


def test_text_to_speech_returns_400_when_text_is_empty() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/text-to-speech",
            json={"text": ""},
        )

    assert response.status_code == 400
    assert response.json() == {"detail": "Text is required"}
