from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Optional

class Settings(BaseSettings):
    # API 配置
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Image Processing Service"
    
    # CORS 配置
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    # 文件上传配置
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set = {'.png', '.jpg', '.jpeg', '.webp'}
    
    # 临时文件配置
    TEMP_DIR: Optional[Path] = None

    class Config:
        case_sensitive = True
        env_prefix = "APP_"  # 环境变量前缀

settings = Settings()