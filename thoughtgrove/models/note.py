from datetime import datetime, UTC
from typing import Optional
from pydantic import BaseModel, Field, field_validator

from thoughtgrove.models.base import BaseDocument


class NoteBase(BaseModel):
    """笔记基础模型"""
    title: str
    content: str
    
    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        if not v or len(v.strip()) == 0:
            raise ValueError("标题不能为空")
        return v
    
    @field_validator("content")
    @classmethod
    def validate_content(cls, v: str) -> str:
        if not v or len(v.strip()) == 0:
            raise ValueError("内容不能为空")
        return v


class NoteCreate(NoteBase):
    """创建笔记模型"""
    user_id: Optional[str] = None
    
    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and len(v.strip()) == 0:
            raise ValueError("用户ID不能为空")
        return v


class NoteUpdate(BaseModel):
    """更新笔记模型"""
    title: Optional[str] = None
    content: Optional[str] = None
    
    @field_validator("title")
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and len(v.strip()) == 0:
            raise ValueError("标题不能为空")
        return v
    
    @field_validator("content")
    @classmethod
    def validate_content(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and len(v.strip()) == 0:
            raise ValueError("内容不能为空")
        return v


class Note(NoteBase):
    """笔记模型"""
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime


class NoteInDB(BaseDocument, NoteBase):
    """数据库笔记模型"""
    user_id: str 