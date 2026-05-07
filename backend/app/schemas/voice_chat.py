from pydantic import BaseModel


class VoiceChatResponse(BaseModel):
    user_text: str
    ai_text: str
    audio_url: str
