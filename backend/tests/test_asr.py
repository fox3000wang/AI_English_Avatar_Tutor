from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import app


def test_speech_to_text_returns_mock_text_without_openai_key(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    get_settings.cache_clear()

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/speech-to-text",
            files={"file": ("hello.wav", b"fake audio bytes", "audio/wav")},
        )

    assert response.status_code == 200
    assert response.json() == {"text": "Hello teacher"}
    get_settings.cache_clear()


def test_speech_to_text_returns_400_when_file_is_missing() -> None:
    with TestClient(app) as client:
        response = client.post("/api/v1/speech-to-text")

    assert response.status_code == 400
    assert response.json() == {"detail": "Audio file is required"}
