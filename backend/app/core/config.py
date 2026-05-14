from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI English Avatar Tutor API"
    app_env: str = "development"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"

    openai_api_key: str = ""
    minimax_api_key: str = ""
    minimax_base_url: str = "https://api.minimaxi.com/v1"
    minimax_chat_model: str = "MiniMax-M2.7"
    minimax_tts_model: str = "speech-2.6-turbo"
    minimax_tts_voice_id: str = "English_Trustworth_Man"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/avatar_tutor"
    redis_url: str = "redis://localhost:6379/0"
    tts_provider: str = "openai"
    asr_provider: str = "openai"
    chat_provider: str = "mock"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
