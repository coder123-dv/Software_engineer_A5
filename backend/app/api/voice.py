"""API路由 - 语音 (ASR/TTS)"""

import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import Response

from app.services.tts_service import text_to_speech
from app.services.asr_service import speech_to_text
from app.config import settings

router = APIRouter(prefix="/api/voice", tags=["语音"])


@router.post("/asr")
async def asr(file: UploadFile = File(...)):
    """语音识别: 上传音频 → 返回文本"""
    audio_data = await file.read()
    content_type = file.content_type or "audio/wav"

    result = await speech_to_text(audio_data, content_type)
    return result


@router.post("/tts")
async def tts(text: str = Form(...), voice_id: str = Form(default=None)):
    """语音合成: 文本 → 返回音频"""
    audio_data = await text_to_speech(text, voice_id)

    if audio_data:
        return Response(
            content=audio_data,
            media_type="audio/mpeg",
            headers={"Content-Disposition": f"attachment; filename={uuid.uuid4()}.mp3"},
        )

    return {"error": "TTS服务未配置或不可用", "text": text}
