"""RAG 服务 - 检索增强生成"""

import json
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.knowledge import KnowledgeChunk, KnowledgeDocument
from app.services.embedding_service import get_embedding, cosine_similarity
from app.config import settings


async def retrieve_relevant_chunks(
    query: str,
    db: AsyncSession,
    top_k: int = None,
) -> list[dict]:
    """混合检索: 向量相似度 + 关键词匹配"""
    top_k = top_k or settings.RAG_TOP_K

    # 获取查询向量
    try:
        query_embedding = await get_embedding(query)
    except Exception:
        # 如果 embedding 服务不可用，回退到关键词检索
        return await _keyword_search(query, db, top_k)

    # 从数据库获取所有活跃的chunks
    stmt = (
        select(KnowledgeChunk)
        .join(KnowledgeDocument)
        .where(KnowledgeDocument.is_active == True)
    )
    result = await db.execute(stmt)
    chunks = result.scalars().all()

    if not chunks:
        return []

    # 向量相似度排序
    scored_chunks = []
    for chunk in chunks:
        if chunk.embedding:
            try:
                chunk_vec = json.loads(chunk.embedding)
                score = cosine_similarity(query_embedding, chunk_vec)
                scored_chunks.append({
                    "chunk_id": chunk.id,
                    "text": chunk.chunk_text,
                    "score": score,
                    "document_id": chunk.document_id,
                    "metadata": json.loads(chunk.metadata_json) if chunk.metadata_json else {},
                })
            except (json.JSONDecodeError, ValueError):
                continue

    # 按分数排序取 Top-K
    scored_chunks.sort(key=lambda x: x["score"], reverse=True)
    return scored_chunks[:top_k]


async def _keyword_search(query: str, db: AsyncSession, top_k: int) -> list[dict]:
    """关键词回退检索 (当embedding服务不可用时)"""
    import jieba

    keywords = list(jieba.cut(query))

    stmt = (
        select(KnowledgeChunk)
        .join(KnowledgeDocument)
        .where(KnowledgeDocument.is_active == True)
    )
    result = await db.execute(stmt)
    chunks = result.scalars().all()

    scored = []
    for chunk in chunks:
        # 简单关键词匹配评分
        score = sum(1 for kw in keywords if kw in chunk.chunk_text and len(kw) > 1)
        if score > 0:
            scored.append({
                "chunk_id": chunk.id,
                "text": chunk.chunk_text,
                "score": score / len(keywords),
                "document_id": chunk.document_id,
                "metadata": json.loads(chunk.metadata_json) if chunk.metadata_json else {},
            })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]


def format_context(chunks: list[dict]) -> str:
    """将检索到的知识片段格式化为LLM上下文"""
    if not chunks:
        return ""
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        source = chunk.get("metadata", {}).get("title", f"知识片段{i}")
        context_parts.append(f"【{source}】\n{chunk['text']}")
    return "\n\n---\n\n".join(context_parts)
