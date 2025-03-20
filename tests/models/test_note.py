from datetime import datetime, UTC
import pytest
from pydantic import ValidationError

from thoughtgrove.models.note import Note, NoteCreate, NoteUpdate, NoteInDB


class TestNote:
    def test_note_create(self):
        """测试创建笔记模型"""
        note_data = {
            "title": "测试笔记",
            "content": "这是一个测试笔记的内容",
            "user_id": "user123"
        }
        note = NoteCreate(**note_data)
        assert note.title == note_data["title"]
        assert note.content == note_data["content"]
        assert note.user_id == note_data["user_id"]
        
    def test_note_create_validation(self):
        """测试笔记模型验证"""
        # 标题为空的情况
        with pytest.raises(ValidationError):
            NoteCreate(title="", content="内容", user_id="user123")
        
        # 内容为空的情况
        with pytest.raises(ValidationError):
            NoteCreate(title="标题", content="", user_id="user123")
            
        # 用户ID为空的情况
        with pytest.raises(ValidationError):
            NoteCreate(title="标题", content="内容", user_id="")
            
    def test_note_in_db(self):
        """测试数据库笔记模型"""
        note_data = {
            "_id": "note123",
            "title": "测试笔记",
            "content": "这是一个测试笔记的内容",
            "user_id": "user123",
            "created_at": datetime.now(UTC),
            "updated_at": datetime.now(UTC)
        }
        note = NoteInDB(**note_data)
        assert note.id == note_data["_id"]
        assert note.title == note_data["title"]
        assert note.content == note_data["content"]
        assert note.user_id == note_data["user_id"]
        
    def test_note_update(self):
        """测试笔记更新模型"""
        # 只更新标题
        update_data = {"title": "更新的标题"}
        note_update = NoteUpdate(**update_data)
        assert note_update.title == update_data["title"]
        assert note_update.content is None
        
        # 只更新内容
        update_data = {"content": "更新的内容"}
        note_update = NoteUpdate(**update_data)
        assert note_update.content == update_data["content"]
        assert note_update.title is None 