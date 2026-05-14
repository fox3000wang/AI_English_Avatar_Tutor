import json
from pathlib import Path
from urllib import request
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
    if settings.tts_provider == "minimax":
        if not settings.minimax_api_key:
            output_path.write_bytes(MOCK_MP3_BYTES)
            return f"{AUDIO_URL_PREFIX}/{filename}"

        output_path.write_bytes(synthesize_minimax_speech(text))
        return f"{AUDIO_URL_PREFIX}/{filename}"

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


def synthesize_minimax_speech(text: str) -> bytes:
    settings = get_settings()
    payload = {
        "model": settings.minimax_tts_model,
        "text": text,
        "stream": False,
        "voice_setting": {
            "voice_id": settings.minimax_tts_voice_id,
            "speed": 1,
            "vol": 1,
            "pitch": 0,
        },
        "audio_setting": {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3",
            "channel": 1,
        },
    }
    tts_url = f"{settings.minimax_base_url.rstrip('/')}/t2a_v2"
    http_request = request.Request(
        tts_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {settings.minimax_api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with request.urlopen(http_request, timeout=60) as response:
        body = json.loads(response.read().decode("utf-8"))

    audio_hex = body.get("data", {}).get("audio")
    if not audio_hex:
        raise ValueError("MiniMax TTS response did not include audio data")

    return bytes.fromhex(audio_hex)
