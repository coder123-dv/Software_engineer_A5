"""Pydantic Schemas - 数据分析"""

from pydantic import BaseModel, Field
from typing import Optional


class DashboardData(BaseModel):
    """数据大屏概览"""
    total_conversations: int = 0
    total_messages: int = 0
    today_conversations: int = 0
    avg_sentiment: float = 0.0
    avg_response_time_ms: int = 0
    satisfaction_score: float = 0.0
    top_questions: list[dict] = Field(default_factory=list)
    daily_trend: list[dict] = Field(default_factory=list)


class SentimentReport(BaseModel):
    """情感分析报告"""
    period: str  # 时间范围
    positive_ratio: float = 0.0
    neutral_ratio: float = 0.0
    negative_ratio: float = 0.0
    trend: list[dict] = Field(default_factory=list)
    keywords: list[dict] = Field(default_factory=list)  # 关键词词频
    suggestions: list[str] = Field(default_factory=list)  # AI建议
