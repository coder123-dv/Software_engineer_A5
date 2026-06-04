"""RAG 索引器 - 文档分块与入库"""

import json
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.knowledge import KnowledgeDocument, KnowledgeChunk
from app.utils.doc_parser import parse_file
from app.services.embedding_service import get_embeddings
from app.config import settings


def chunk_text(text: str, chunk_size: int = None, overlap: int = None) -> list[str]:
    """智能文本分块

    Args:
        text: 原始文本
        chunk_size: 每块最大字符数
        overlap: 重叠字符数

    Returns:
        文本块列表
    """
    chunk_size = chunk_size or settings.CHUNK_SIZE
    overlap = overlap or settings.CHUNK_OVERLAP

    if len(text) <= chunk_size:
        return [text]

    chunks = []
    # 按句号/换行分割，然后组合到chunk_size
    sentences = []
    for line in text.replace("。", "。\n").split("\n"):
        line = line.strip()
        if line:
            sentences.append(line)

    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) > chunk_size and current_chunk:
            chunks.append(current_chunk)
            # 保留overlap
            if overlap > 0:
                current_chunk = current_chunk[-overlap:] + sentence
            else:
                current_chunk = sentence
        else:
            current_chunk += sentence

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


async def index_document(
    doc: KnowledgeDocument,
    db: AsyncSession,
    generate_embeddings: bool = True,
) -> int:
    """将文档内容分块并生成向量索引

    Returns:
        创建的chunk数量
    """
    # 文本分块
    chunks_text = chunk_text(doc.content)

    # 批量生成embedding
    embeddings = []
    if generate_embeddings:
        try:
            embeddings = await get_embeddings(chunks_text)
        except Exception:
            # embedding服务不可用时跳过
            embeddings = [None] * len(chunks_text)
    else:
        embeddings = [None] * len(chunks_text)

    # 入库
    chunk_count = 0
    for i, (text, emb) in enumerate(zip(chunks_text, embeddings)):
        chunk = KnowledgeChunk(
            document_id=doc.id,
            chunk_text=text,
            chunk_index=i,
            embedding=json.dumps(emb) if emb else None,
            metadata_json=json.dumps({"title": doc.title, "category": doc.category}, ensure_ascii=False),
        )
        db.add(chunk)
        chunk_count += 1

    await db.flush()
    return chunk_count


async def index_file(
    file_path: str | Path,
    title: str,
    category: str,
    db: AsyncSession,
) -> KnowledgeDocument:
    """解析文件并创建知识文档+索引"""
    sections = parse_file(file_path)

    # 合并所有文本作为文档内容
    full_content = "\n\n".join(s["text"] for s in sections)

    # 创建文档记录
    doc = KnowledgeDocument(
        title=title,
        category=category,
        content=full_content,
        source_file=Path(file_path).name,
    )
    db.add(doc)
    await db.flush()  # 获取doc.id

    # 索引分块
    await index_document(doc, db)

    return doc
