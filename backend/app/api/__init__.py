"""API 路由注册"""

from fastapi import APIRouter

from app.api.chat import router as chat_router
from app.api.voice import router as voice_router
from app.api.knowledge import router as knowledge_router
from app.api.auth import router as auth_router
from app.api.avatar import router as avatar_router
from app.api.analytics import router as analytics_router
from app.api.recommend import router as recommend_router

api_router = APIRouter()

api_router.include_router(chat_router)
api_router.include_router(voice_router)
api_router.include_router(knowledge_router)
api_router.include_router(auth_router)
api_router.include_router(avatar_router)
api_router.include_router(analytics_router)
api_router.include_router(recommend_router)
