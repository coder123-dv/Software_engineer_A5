"""全局配置 - 所有AI服务通过 base_url + api_key 接入"""

from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    # === LLM 大模型 ===
    LLM_BASE_URL: str = "https://api.openai.com/v1"
    LLM_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4o-mini"

    # === Embedding 向量模型 ===
    EMBEDDING_BASE_URL: str = "https://api.openai.com/v1"
    EMBEDDING_API_KEY: str = ""
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    EMBEDDING_DIM: int = 1536

    # === TTS 语音合成 ===
    TTS_BASE_URL: str = ""
    TTS_API_KEY: str = ""
    TTS_VOICE: str = "zh-CN-XiaoxiaoNeural"

    # === ASR 语音识别 ===
    ASR_BASE_URL: str = ""
    ASR_API_KEY: str = ""

    # === 数据库 ===
    DATABASE_URL: str = "sqlite+aiosqlite:///./storage/db.sqlite3"

    # === JWT 认证 ===
    SECRET_KEY: str = "scenic-guide-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480

    # === 应用 ===
    APP_NAME: str = "景区导览服务AI数字人"
    DEBUG: bool = False
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000", "http://localhost"]

    # === RAG 配置 ===
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 64
    RAG_TOP_K: int = 3

    # === 文件路径 ===
    UPLOAD_DIR: Path = Path("./storage/uploads")
    DATA_DIR: Path = Path("./data")

    model_config = {"env_file": "../.env", "env_file_encoding": "utf-8", "extra": "ignore"}


settings = Settings()
