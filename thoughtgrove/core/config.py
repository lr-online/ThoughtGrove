from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    """应用配置"""
    # MongoDB配置
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "thoughtgrove"
    
    # OpenAI配置
    openai_api_key: str = "your_openai_api_key_here"
    
    # JWT配置
    jwt_secret_key: str = "your_jwt_secret_key_here"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # 应用配置
    app_env: str = "development"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"
    
    # 日志配置
    log_level: str = "INFO"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
        env_prefix=""
    )

@lru_cache()
def get_settings() -> Settings:
    """获取应用配置单例"""
    return Settings() 