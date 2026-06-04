"""Pydantic Schemas - 知识库"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class KnowledgeCreate(BaseModel):
    title: str = Field(..., description="文档标题")
    category: str = Field(default="general", description="分类: scenic_intro/history/culture/faq/route")
    content: str = Field(..., description="文档内容")
    source_file: str = Field(default="", description="来源文件名")


class KnowledgeUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    content: Optional[str] = None
    is_active: Optional[bool] = None


class KnowledgeOut(BaseModel):
    id: int
    title: str
    category: str
    content: str
    source_file: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    chunk_count: int = 0

    model_config = {"from_attributes": True}


class KnowledgeListOut(BaseModel):
    id: int
    title: str
    category: str
    source_file: str
    is_active: bool
    created_at: datetime
    chunk_count: int = 0

    model_config = {"from_attributes": True}
