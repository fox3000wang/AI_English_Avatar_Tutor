from fastapi import APIRouter, HTTPException

from app.schemas.tts import TextToSpeechRequest, TextToSpeechResponse
from app.services.tts_service import synthesize_speech

router = APIRouter(tags=["tts"])


@router.post("/text-to-speech", response_model=TextToSpeechResponse)
async def text_to_speech(request: TextToSpeechRequest) -> TextToSpeechResponse:
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text is required")

    audio_url = synthesize_speech(text)
    return TextToSpeechResponse(audio_url=audio_url)
