"""ORM 模型 - 统计数据"""

from datetime import date, datetime
from sqlalchemy import String, Text, Integer, Float, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class DailyStats(Base):
    """每日统计聚合"""
    __tablename__ = "daily_stats"

    id: Mapped[int] = mapped_column(primary_key=True)
    stat_date: Mapped[date] = mapped_column(Date, unique=True)
    total_conversations: Mapped[int] = mapped_column(Integer, default=0)
    total_messages: Mapped[int] = mapped_column(Integer, default=0)
    avg_sentiment: Mapped[float] = mapped_column(Float, default=0.0)
    avg_response_time_ms: Mapped[int] = mapped_column(Integer, default=0)
    top_questions: Mapped[str] = mapped_column(Text, default="[]")  # JSON array
    satisfaction_score: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
