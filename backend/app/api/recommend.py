"""API路由 - 路线推荐"""

import json
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field

from app.database import get_db
from app.services.llm_service import chat_completion

router = APIRouter(prefix="/api/recommend", tags=["路线推荐"])


class RecommendRequest(BaseModel):
    interests: list[str] = Field(default_factory=list, description="兴趣标签")
    duration: str = Field(default="half_day", description="游览时长: half_day/full_day/two_days")
    pace: str = Field(default="normal", description="节奏: fast/normal/leisurely")


class RecommendResponse(BaseModel):
    route_name: str
    description: str
    spots: list[dict]
    estimated_time: str
    tips: str


# 预定义路线 (基于灵山胜境景区)
PRESET_ROUTES = {
    "经典全览": {
        "route_name": "经典全览路线",
        "description": "一日游览灵山胜境核心景点，感受佛教文化的博大精深",
        "spots": [
            {"name": "九龙灌浴", "duration": "30min", "highlight": "大型动态音乐群雕"},
            {"name": "灵山大佛", "duration": "60min", "highlight": "88米高青铜大佛"},
            {"name": "梵宫", "duration": "90min", "highlight": "东方卢浮宫，华丽殿堂"},
            {"name": "五印坛城", "duration": "45min", "highlight": "藏传佛教文化体验"},
            {"name": "拈花湾", "duration": "120min", "highlight": "禅意小镇，休闲漫步"},
        ],
        "estimated_time": "6-7小时",
        "tips": "建议早上8:30入园，先看九龙灌浴表演（整点开始）",
    },
    "文化深度": {
        "route_name": "文化深度路线",
        "description": "深入了解灵山的历史文化底蕴",
        "spots": [
            {"name": "灵山大佛", "duration": "90min", "highlight": "了解大佛建造历史"},
            {"name": "祥符禅寺", "duration": "60min", "highlight": "千年古刹，佛教圣地"},
            {"name": "梵宫", "duration": "120min", "highlight": "观看《灵山吉祥颂》演出"},
            {"name": "百子戏弥勒", "duration": "30min", "highlight": "青铜雕塑群"},
        ],
        "estimated_time": "5-6小时",
        "tips": "《灵山吉祥颂》演出时间请提前查询，建议预留充足时间",
    },
    "亲子休闲": {
        "route_name": "亲子休闲路线",
        "description": "适合家庭出游，节奏轻松",
        "spots": [
            {"name": "九龙灌浴", "duration": "30min", "highlight": "孩子们最喜欢的水景表演"},
            {"name": "灵山大佛", "duration": "45min", "highlight": "登顶俯瞰太湖美景"},
            {"name": "拈花湾", "duration": "180min", "highlight": "亲子手工、禅意体验"},
        ],
        "estimated_time": "4-5小时",
        "tips": "拈花湾有丰富的亲子活动，建议下午前往",
    },
}


@router.post("", response_model=RecommendResponse)
async def recommend_route(request: RecommendRequest, db: AsyncSession = Depends(get_db)):
    """根据偏好推荐游览路线"""
    # 简单匹配逻辑
    if "历史" in request.interests or "文化" in request.interests or "佛教" in request.interests:
        route = PRESET_ROUTES["文化深度"]
    elif "亲子" in request.interests or "休闲" in request.interests or "家庭" in request.interests:
        route = PRESET_ROUTES["亲子休闲"]
    else:
        route = PRESET_ROUTES["经典全览"]

    # 根据时长调整
    if request.duration == "half_day" and len(route["spots"]) > 3:
        route = dict(route)
        route["spots"] = route["spots"][:3]
        route["estimated_time"] = "3-4小时"

    return RecommendResponse(**route)
