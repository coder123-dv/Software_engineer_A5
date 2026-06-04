"""API路由 - 数字人形象管理"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.avatar import AvatarConfig
from app.schemas.avatar import AvatarConfigOut, AvatarConfigUpdate

router = APIRouter(prefix="/api/avatar", tags=["数字人形象"])


@router.get("", response_model=list[AvatarConfigOut])
async def list_avatars(db: AsyncSession = Depends(get_db)):
    """获取所有数字人形象"""
    result = await db.execute(select(AvatarConfig))
    return result.scalars().all()


@router.get("/default", response_model=AvatarConfigOut)
async def get_default_avatar(db: AsyncSession = Depends(get_db)):
    """获取默认数字人形象"""
    result = await db.execute(select(AvatarConfig).where(AvatarConfig.is_default == True))
    avatar = result.scalar_one_or_none()
    if not avatar:
        # 创建默认配置
        avatar = AvatarConfig(
            name="小灵",
            personality="你是灵山胜境的AI导游小灵，热情友善、知识渊博，善于用生动的语言描述景区特色。",
            greeting="您好！我是灵山胜境的AI导游小灵，很高兴为您服务！有什么想了解的吗？",
            is_default=True,
        )
        db.add(avatar)
        await db.flush()
    return avatar


@router.put("/{avatar_id}", response_model=AvatarConfigOut)
async def update_avatar(avatar_id: int, data: AvatarConfigUpdate, db: AsyncSession = Depends(get_db)):
    """更新数字人配置"""
    result = await db.execute(select(AvatarConfig).where(AvatarConfig.id == avatar_id))
    avatar = result.scalar_one_or_none()
    if not avatar:
        raise HTTPException(status_code=404, detail="形象配置不存在")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(avatar, key, value)

    return avatar
