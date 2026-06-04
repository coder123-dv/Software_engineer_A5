"""API路由 - 数据分析"""

from datetime import date, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database import get_db
from app.models.conversation import Conversation, Message
from app.schemas.analytics import DashboardData, SentimentReport

router = APIRouter(prefix="/api/analytics", tags=["数据分析"])


@router.get("/dashboard", response_model=DashboardData)
async def get_dashboard(db: AsyncSession = Depends(get_db)):
    """数据大屏概览"""
    # 总会话数
    total_conv = await db.execute(select(func.count(Conversation.id)))
    total_conversations = total_conv.scalar() or 0

    # 总消息数
    total_msg = await db.execute(select(func.count(Message.id)))
    total_messages = total_msg.scalar() or 0

    # 今日会话数
    today = date.today()
    today_conv = await db.execute(
        select(func.count(Conversation.id))
        .where(func.date(Conversation.started_at) == today)
    )
    today_conversations = today_conv.scalar() or 0

    # 平均情感得分
    avg_sent = await db.execute(
        select(func.avg(Message.sentiment_score))
        .where(Message.role == "user")
    )
    avg_sentiment = round(avg_sent.scalar() or 0, 2)

    # 平均响应时间
    avg_rt = await db.execute(
        select(func.avg(Message.response_time_ms))
        .where(Message.role == "assistant")
    )
    avg_response_time_ms = int(avg_rt.scalar() or 0)

    # 最近7天趋势
    daily_trend = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        day_count = await db.execute(
            select(func.count(Conversation.id))
            .where(func.date(Conversation.started_at) == d)
        )
        daily_trend.append({"date": d.isoformat(), "count": day_count.scalar() or 0})

    # 热门问题 (最近的用户消息)
    top_q = await db.execute(
        select(Message.content)
        .where(Message.role == "user")
        .order_by(Message.created_at.desc())
        .limit(10)
    )
    top_questions = [{"question": q, "count": 1} for q in top_q.scalars().all()]

    return DashboardData(
        total_conversations=total_conversations,
        total_messages=total_messages,
        today_conversations=today_conversations,
        avg_sentiment=avg_sentiment,
        avg_response_time_ms=avg_response_time_ms,
        satisfaction_score=max(0, (avg_sentiment + 1) * 50),  # 转为0-100分
        top_questions=top_questions[:5],
        daily_trend=daily_trend,
    )


@router.get("/sentiment", response_model=SentimentReport)
async def get_sentiment_report(days: int = 7, db: AsyncSession = Depends(get_db)):
    """情感分析报告"""
    since = date.today() - timedelta(days=days)

    # 各情感占比
    total = await db.execute(
        select(func.count(Message.id))
        .where(Message.role == "user", func.date(Message.created_at) >= since)
    )
    total_count = total.scalar() or 1

    pos = await db.execute(
        select(func.count(Message.id))
        .where(Message.role == "user", Message.sentiment_label == "positive",
               func.date(Message.created_at) >= since)
    )
    neg = await db.execute(
        select(func.count(Message.id))
        .where(Message.role == "user", Message.sentiment_label == "negative",
               func.date(Message.created_at) >= since)
    )

    pos_count = pos.scalar() or 0
    neg_count = neg.scalar() or 0
    neu_count = total_count - pos_count - neg_count

    return SentimentReport(
        period=f"最近{days}天",
        positive_ratio=round(pos_count / total_count, 2),
        neutral_ratio=round(neu_count / total_count, 2),
        negative_ratio=round(neg_count / total_count, 2),
        trend=[],
        keywords=[],
        suggestions=["持续保持良好的服务质量", "关注游客高频问题，优化知识库内容"],
    )
