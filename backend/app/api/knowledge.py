"""API路由 - 知识库管理"""

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database import get_db
from app.models.knowledge import KnowledgeDocument, KnowledgeChunk
from app.schemas.knowledge import KnowledgeCreate, KnowledgeUpdate, KnowledgeOut, KnowledgeListOut
from app.rag.indexer import index_document, index_file
from app.config import settings

router = APIRouter(prefix="/api/knowledge", tags=["知识库"])


@router.get("", response_model=list[KnowledgeListOut])
async def list_documents(
    category: str = None,
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
):
    """获取知识库文档列表"""
    stmt = select(KnowledgeDocument)
    if category:
        stmt = stmt.where(KnowledgeDocument.category == category)
    stmt = stmt.order_by(KnowledgeDocument.created_at.desc()).offset(skip).limit(limit)

    result = await db.execute(stmt)
    docs = result.scalars().all()

    # 获取每个文档的chunk数量
    out = []
    for doc in docs:
        chunk_count_result = await db.execute(
            select(func.count(KnowledgeChunk.id)).where(KnowledgeChunk.document_id == doc.id)
        )
        chunk_count = chunk_count_result.scalar() or 0
        out.append(KnowledgeListOut(
            id=doc.id,
            title=doc.title,
            category=doc.category,
            source_file=doc.source_file,
            is_active=doc.is_active,
            created_at=doc.created_at,
            chunk_count=chunk_count,
        ))

    return out


@router.get("/{doc_id}", response_model=KnowledgeOut)
async def get_document(doc_id: int, db: AsyncSession = Depends(get_db)):
    """获取单个文档详情"""
    result = await db.execute(select(KnowledgeDocument).where(KnowledgeDocument.id == doc_id))
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="文档不存在")

    chunk_count_result = await db.execute(
        select(func.count(KnowledgeChunk.id)).where(KnowledgeChunk.document_id == doc.id)
    )
    chunk_count = chunk_count_result.scalar() or 0

    return KnowledgeOut(
        id=doc.id,
        title=doc.title,
        category=doc.category,
        content=doc.content,
        source_file=doc.source_file,
        is_active=doc.is_active,
        created_at=doc.created_at,
        updated_at=doc.updated_at,
        chunk_count=chunk_count,
    )


@router.post("", response_model=KnowledgeOut)
async def create_document(data: KnowledgeCreate, db: AsyncSession = Depends(get_db)):
    """创建知识文档 (手动输入)"""
    doc = KnowledgeDocument(
        title=data.title,
        category=data.category,
        content=data.content,
        source_file=data.source_file,
    )
    db.add(doc)
    await db.flush()

    # 自动索引
    chunk_count = await index_document(doc, db, generate_embeddings=True)

    return KnowledgeOut(
        id=doc.id,
        title=doc.title,
        category=doc.category,
        content=doc.content,
        source_file=doc.source_file,
        is_active=doc.is_active,
        created_at=doc.created_at,
        updated_at=doc.updated_at,
        chunk_count=chunk_count,
    )


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(default=""),
    category: str = Form(default="general"),
    db: AsyncSession = Depends(get_db),
):
    """上传文档文件 (docx/xlsx/txt)"""
    # 保存文件
    settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    file_path = settings.UPLOAD_DIR / file.filename
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    # 解析并索引
    doc_title = title or file.filename.rsplit(".", 1)[0]
    try:
        doc = await index_file(file_path, doc_title, category, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": "上传成功", "document_id": doc.id, "title": doc.title}


@router.put("/{doc_id}", response_model=KnowledgeOut)
async def update_document(doc_id: int, data: KnowledgeUpdate, db: AsyncSession = Depends(get_db)):
    """更新知识文档"""
    result = await db.execute(select(KnowledgeDocument).where(KnowledgeDocument.id == doc_id))
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="文档不存在")

    # 更新字段
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(doc, key, value)

    # 如果内容更新了，重新索引
    if "content" in update_data:
        # 删除旧chunks
        await db.execute(
            select(KnowledgeChunk).where(KnowledgeChunk.document_id == doc.id)
        )
        from sqlalchemy import delete
        await db.execute(delete(KnowledgeChunk).where(KnowledgeChunk.document_id == doc.id))
        # 重新索引
        await index_document(doc, db)

    chunk_count_result = await db.execute(
        select(func.count(KnowledgeChunk.id)).where(KnowledgeChunk.document_id == doc.id)
    )
    chunk_count = chunk_count_result.scalar() or 0

    return KnowledgeOut(
        id=doc.id, title=doc.title, category=doc.category, content=doc.content,
        source_file=doc.source_file, is_active=doc.is_active,
        created_at=doc.created_at, updated_at=doc.updated_at, chunk_count=chunk_count,
    )


@router.delete("/{doc_id}")
async def delete_document(doc_id: int, db: AsyncSession = Depends(get_db)):
    """删除知识文档"""
    result = await db.execute(select(KnowledgeDocument).where(KnowledgeDocument.id == doc_id))
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="文档不存在")

    await db.delete(doc)
    return {"message": "删除成功"}
