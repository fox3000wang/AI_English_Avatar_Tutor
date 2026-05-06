from pydantic import BaseModel


class TextToSpeechRequest(BaseModel):
    text: str


class TextToSpeechResponse(BaseModel):
    audio_url: str
