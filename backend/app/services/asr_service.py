from io import BytesIO

from app.core.config import get_settings

MOCK_TRANSCRIPT = "Hello teacher"
WHISPER_MODEL = "whisper-1"


def transcribe_audio(audio_bytes: bytes, filename: str, content_type: str | None = None) -> str:
    settings = get_settings()
    if not settings.openai_api_key:
        return MOCK_TRANSCRIPT

    from openai import OpenAI

    client = OpenAI(api_key=settings.openai_api_key)
    audio_file = BytesIO(audio_bytes)
    audio_file.name = filename

    transcription = client.audio.transcriptions.create(
        model=WHISPER_MODEL,
        file=(filename, audio_file, content_type or "application/octet-stream"),
    )
    return transcription.text
