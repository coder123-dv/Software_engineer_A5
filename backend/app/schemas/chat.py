"""Pydantic Schemas - 对话"""

from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    message: str = Field(..., description="用户输入文本")
    conversation_id: Optional[str] = Field(None, description="会话ID，为空则新建")
    visitor_id: str = Field(default="anonymous", description="游客ID")


class VisemeKeyframe(BaseModel):
    time: float = Field(..., description="时间戳(秒)")
    viseme: str = Field(..., description="Viseme类型")
    weight: float = Field(default=1.0, description="权重 0-1")


class ChatResponse(BaseModel):
    reply: str = Field(..., description="AI回复文本")
    conversation_id: str = Field(..., description="会话ID")
    audio_url: Optional[str] = Field(None, description="TTS音频URL")
    viseme_timeline: list[VisemeKeyframe] = Field(default_factory=list, description="口型时间轴")
    expression: str = Field(default="neutral", description="表情建议")
    sentiment: dict = Field(default_factory=lambda: {"score": 0.0, "label": "neutral"})
    sources: list[str] = Field(default_factory=list, description="引用知识来源")


class MessageOut(BaseModel):
    role: str
    content: str
    sentiment_label: str = "neutral"
    created_at: str

    model_config = {"from_attributes": True}
