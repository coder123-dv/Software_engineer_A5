"""TTS 语音合成服务"""

import httpx
from app.config import settings


async def text_to_speech(text: str, voice_id: str = None) -> bytes | None:
    """文本转语音

    Args:
        text: 要合成的文本
        voice_id: 声音ID

    Returns:
        音频二进制数据 (WAV/MP3), 如果TTS服务未配置则返回None
    """
    if not settings.TTS_BASE_URL or not settings.TTS_API_KEY:
        return None

    voice = voice_id or settings.TTS_VOICE

    # 通用TTS API调用 (兼容多种TTS服务)
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                f"{settings.TTS_BASE_URL}/audio/speech",
                headers={
                    "Authorization": f"Bearer {settings.TTS_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "tts-1",
                    "input": text,
                    "voice": voice,
                    "response_format": "mp3",
                },
            )
            if response.status_code == 200:
                return response.content
        except Exception:
            pass

    return None
