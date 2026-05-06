from pathlib import Path
from uuid import uuid4

from app.core.config import get_settings

AUDIO_STORAGE_DIR = Path(__file__).resolve().parents[2] / "storage" / "audio"
AUDIO_URL_PREFIX = "/storage/audio"
MOCK_MP3_BYTES = b"mock mp3 audio bytes"
TTS_MODEL = "gpt-4o-mini-tts"
TTS_VOICE = "coral"
TTS_INSTRUCTIONS = "Speak like a warm, encouraging female English teacher for a child."


def synthesize_speech(text: str) -> str:
    AUDIO_STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid4()}.mp3"
    output_path = AUDIO_STORAGE_DIR / filename

    settings = get_settings()
    if not settings.openai_api_key:
        output_path.write_bytes(MOCK_MP3_BYTES)
        return f"{AUDIO_URL_PREFIX}/{filename}"

    from openai import OpenAI

    client = OpenAI(api_key=settings.openai_api_key)
    with client.audio.speech.with_streaming_response.create(
        model=TTS_MODEL,
        voice=TTS_VOICE,
        input=text,
        instructions=TTS_INSTRUCTIONS,
        response_format="mp3",
    ) as response:
        response.stream_to_file(output_path)

    return f"{AUDIO_URL_PREFIX}/{filename}"
