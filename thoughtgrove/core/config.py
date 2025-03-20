from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # MongoDB配置
    mongodb_url: str
    mongodb_db_name: str
    
    # OpenAI配置
    openai_api_key: str
    
    # JWT配置
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # 应用配置
    app_env: str = "development"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"
    
    # 日志配置
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings() 