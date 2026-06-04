"""API路由 - 对话"""

import time
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.models.conversation import Conversation, Message
from app.models.avatar import AvatarConfig
from app.services.llm_service import chat_completion
from app.services.rag_service import retrieve_relevant_chunks, format_context
from app.services.viseme_service import text_to_viseme_timeline
from app.services.sentiment_service import analyze_sentiment, get_expression_from_sentiment

router = APIRouter(prefix="/api/chat", tags=["对话"])


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    """文本对话接口 - 核心接口"""
    start_time = time.time()

    # 获取或创建会话
    conversation_id = request.conversation_id
    if not conversation_id:
        conversation = Conversation(visitor_id=request.visitor_id)
        db.add(conversation)
        await db.flush()
        conversation_id = conversation.id
    else:
        result = await db.execute(select(Conversation).where(Conversation.id == conversation_id))
        conversation = result.scalar_one_or_none()
        if not conversation:
            conversation = Conversation(id=conversation_id, visitor_id=request.visitor_id)
            db.add(conversation)
            await db.flush()

    # 获取对话历史
    result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.desc())
        .limit(10)
    )
    history_msgs = result.scalars().all()
    history = [{"role": m.role, "content": m.content} for m in reversed(history_msgs)]

    # RAG 检索
    chunks = await retrieve_relevant_chunks(request.message, db)
    context = format_context(chunks)
    sources = [c.get("metadata", {}).get("title", "") for c in chunks if c.get("metadata", {}).get("title")]

    # 获取数字人配置
    result = await db.execute(select(AvatarConfig).where(AvatarConfig.is_default == True))
    avatar = result.scalar_one_or_none()
    avatar_name = avatar.name if avatar else "小灵"
    personality = avatar.personality if avatar else "热情友善，知识渊博。"

    # LLM 生成回复
    try:
        reply = await chat_completion(
            message=request.message,
            context=context,
            history=history,
            avatar_name=avatar_name,
            personality=personality,
        )
    except Exception as e:
        reply = f"抱歉，我暂时无法回答您的问题。请稍后再试。(错误: {str(e)[:50]})"

    # 情感分析
    user_sentiment = analyze_sentiment(request.message)
    reply_sentiment = analyze_sentiment(reply)
    expression = get_expression_from_sentiment(reply_sentiment)

    # 生成口型时间轴
    viseme_timeline = text_to_viseme_timeline(reply)

    # 计算响应时间
    response_time_ms = int((time.time() - start_time) * 1000)

    # 保存消息记录
    user_msg = Message(
        conversation_id=conversation_id,
        role="user",
        content=request.message,
        sentiment_score=user_sentiment["score"],
        sentiment_label=user_sentiment["label"],
    )
    assistant_msg = Message(
        conversation_id=conversation_id,
        role="assistant",
        content=reply,
        sentiment_score=reply_sentiment["score"],
        sentiment_label=reply_sentiment["label"],
        response_time_ms=response_time_ms,
    )
    db.add(user_msg)
    db.add(assistant_msg)

    # 更新会话统计
    conversation.message_count = (conversation.message_count or 0) + 2

    return ChatResponse(
        reply=reply,
        conversation_id=conversation_id,
        audio_url=None,  # TTS由前端单独请求
        viseme_timeline=viseme_timeline,
        expression=expression,
        sentiment=user_sentiment,
        sources=sources,
    )
