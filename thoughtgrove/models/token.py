from pydantic import BaseModel

class Token(BaseModel):
    """认证令牌模型"""
    access_token: str
    token_type: str 