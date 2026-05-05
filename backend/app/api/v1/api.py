from fastapi import APIRouter

from app.api.v1.routes import asr, chat, health, lesson_sessions, lessons, parent_settings

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(asr.router)
api_router.include_router(chat.router)
api_router.include_router(health.router)
api_router.include_router(lesson_sessions.router)
api_router.include_router(lessons.router)
api_router.include_router(parent_settings.router)
