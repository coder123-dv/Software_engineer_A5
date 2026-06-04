"""ASR 语音识别服务"""

import httpx
from app.config import settings


async def speech_to_text(audio_data: bytes, content_type: str = "audio/wav") -> dict:
    """语音转文字

    Args:
        audio_data: 音频二进制数据
        content_type: 音频MIME类型

    Returns:
        {"text": "识别文本", "confidence": 0.95, "duration_ms": 2300}
    """
    if not settings.ASR_BASE_URL or not settings.ASR_API_KEY:
        return {"text": "", "confidence": 0.0, "duration_ms": 0, "error": "ASR服务未配置"}

    # 通用ASR API调用 (OpenAI Whisper兼容接口)
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # 确定文件扩展名
            ext = "wav" if "wav" in content_type else "webm" if "webm" in content_type else "mp3"

            response = await client.post(
                f"{settings.ASR_BASE_URL}/audio/transcriptions",
                headers={
                    "Authorization": f"Bearer {settings.ASR_API_KEY}",
                },
                files={
                    "file": (f"audio.{ext}", audio_data, content_type),
                },
                data={
                    "model": "whisper-1",
                    "language": "zh",
                },
            )
            if response.status_code == 200:
                result = response.json()
                return {
                    "text": result.get("text", ""),
                    "confidence": 0.95,
                    "duration_ms": 0,
                }
        except Exception as e:
            return {"text": "", "confidence": 0.0, "duration_ms": 0, "error": str(e)}

    return {"text": "", "confidence": 0.0, "duration_ms": 0, "error": "ASR请求失败"}
