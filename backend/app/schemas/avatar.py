"""Pydantic Schemas - 数字人形象"""

from pydantic import BaseModel, Field
from typing import Optional


class AvatarConfigOut(BaseModel):
    id: int
    name: str
    vrm_model_url: str
    voice_id: str
    voice_speed: float
    voice_pitch: float
    personality: str
    greeting: str
    is_default: bool

    model_config = {"from_attributes": True}


class AvatarConfigUpdate(BaseModel):
    name: Optional[str] = None
    vrm_model_url: Optional[str] = None
    voice_id: Optional[str] = None
    voice_speed: Optional[float] = None
    voice_pitch: Optional[float] = None
    personality: Optional[str] = None
    greeting: Optional[str] = None
    is_default: Optional[bool] = None
