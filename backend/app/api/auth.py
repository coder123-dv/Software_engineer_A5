"""API路由 - 认证"""

from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException
from jose import jwt

from app.schemas.auth import LoginRequest, TokenResponse
from app.config import settings

router = APIRouter(prefix="/api/auth", tags=["认证"])

# 默认管理员账号 (生产环境应从数据库读取)
ADMIN_USERS = {
    "admin": "admin123",
}


def create_access_token(data: dict) -> str:
    """创建JWT token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """管理员登录"""
    if request.username not in ADMIN_USERS:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    if ADMIN_USERS[request.username] != request.password:
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    token = create_access_token({"sub": request.username})
    return TokenResponse(access_token=token)


@router.get("/me")
async def get_current_user():
    """获取当前用户信息 (简化版)"""
    return {"username": "admin", "role": "admin"}
