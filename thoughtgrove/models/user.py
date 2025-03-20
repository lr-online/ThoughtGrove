from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from thoughtgrove.models.base import BaseDocument

class UserBase(BaseModel):
    """用户基础模型"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False

class UserCreate(UserBase):
    """用户创建模型"""
    password: str = Field(..., min_length=8)

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """验证密码强度"""
        if len(v) < 8:
            raise ValueError('密码长度至少为8个字符')
        if not any(c.isupper() for c in v):
            raise ValueError('密码必须包含至少一个大写字母')
        if not any(c.islower() for c in v):
            raise ValueError('密码必须包含至少一个小写字母')
        if not any(c.isdigit() for c in v):
            raise ValueError('密码必须包含至少一个数字')
        return v

class UserUpdate(BaseModel):
    """用户更新模型"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: Optional[str]) -> Optional[str]:
        """验证密码强度"""
        if v is None:
            return v
        if len(v) < 8:
            raise ValueError('密码长度至少为8个字符')
        if not any(c.isupper() for c in v):
            raise ValueError('密码必须包含至少一个大写字母')
        if not any(c.islower() for c in v):
            raise ValueError('密码必须包含至少一个小写字母')
        if not any(c.isdigit() for c in v):
            raise ValueError('密码必须包含至少一个数字')
        return v

class UserInDB(UserBase, BaseDocument):
    """数据库中的用户模型"""
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        from_attributes=True
    )

class User(UserBase, BaseDocument):
    pass 