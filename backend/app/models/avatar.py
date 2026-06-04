"""ORM 模型 - 数字人形象配置"""

from datetime import datetime
from sqlalchemy import String, Text, Float, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AvatarConfig(Base):
    """数字人形象配置"""
    __tablename__ = "avatar_configs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    vrm_model_url: Mapped[str] = mapped_column(String(500), default="/models/guide.vrm")
    voice_id: Mapped[str] = mapped_column(String(100), default="zh-CN-XiaoxiaoNeural")
    voice_speed: Mapped[float] = mapped_column(Float, default=1.0)
    voice_pitch: Mapped[float] = mapped_column(Float, default=1.0)
    personality: Mapped[str] = mapped_column(Text, default="你是灵山胜境的AI导游，热情友善，知识渊博。")
    greeting: Mapped[str] = mapped_column(Text, default="您好！我是灵山胜境的AI导游小灵，很高兴为您服务！")
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
