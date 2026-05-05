from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.asr import SpeechToTextResponse
from app.services.asr_service import transcribe_audio

router = APIRouter(tags=["asr"])

SUPPORTED_AUDIO_EXTENSIONS = {".mp3", ".wav"}


def is_supported_audio_filename(filename: str) -> bool:
    return any(filename.lower().endswith(extension) for extension in SUPPORTED_AUDIO_EXTENSIONS)


@router.post("/speech-to-text", response_model=SpeechToTextResponse)
async def speech_to_text(
    file: Annotated[UploadFile | None, File()] = None,
) -> SpeechToTextResponse:
    if file is None:
        raise HTTPException(status_code=400, detail="Audio file is required")

    if not is_supported_audio_filename(file.filename or ""):
        raise HTTPException(status_code=400, detail="Only wav and mp3 audio files are supported")

    audio_bytes = await file.read()
    text = transcribe_audio(
        audio_bytes=audio_bytes,
        filename=file.filename or "audio",
        content_type=file.content_type,
    )
    return SpeechToTextResponse(text=text)
