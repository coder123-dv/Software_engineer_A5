"""ORM 模型 - 游客画像"""

from datetime import datetime
from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class VisitorProfile(Base):
    """游客画像"""
    __tablename__ = "visitor_profiles"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    preferences: Mapped[str] = mapped_column(Text, default='{"interests": [], "pace": "normal"}')
    visit_history: Mapped[str] = mapped_column(Text, default="[]")  # JSON: 已浏览景点
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
