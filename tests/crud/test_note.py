import pytest
from bson import ObjectId

from thoughtgrove.models.note import NoteCreate, NoteUpdate
from thoughtgrove.crud.note import create_note, get_note, update_note, delete_note, get_notes_by_user


@pytest.fixture
async def test_note(db):
    """创建测试笔记并在测试后删除"""
    note_data = {
        "title": "测试笔记",
        "content": "这是测试笔记内容",
        "user_id": "test_user"
    }
    note_in = NoteCreate(**note_data)
    note = await create_note(db, note_in)
    yield note
    
    # 测试后清理
    await db.notes.delete_many({"user_id": "test_user"})


class TestNoteCRUD:
    async def test_create_note(self, db):
        """测试创建笔记"""
        note_data = {
            "title": "创建测试笔记",
            "content": "这是创建测试的笔记内容",
            "user_id": "test_user"
        }
        note_in = NoteCreate(**note_data)
        note = await create_note(db, note_in)
        
        assert note.id is not None
        assert note.title == note_data["title"]
        assert note.content == note_data["content"]
        assert note.user_id == note_data["user_id"]
        
        # 清理
        await db.notes.delete_one({"_id": ObjectId(note.id)})
    
    async def test_get_note(self, db, test_note):
        """测试获取笔记"""
        note = await get_note(db, test_note.id)
        
        assert note is not None
        assert note.id == test_note.id
        assert note.title == test_note.title
        assert note.content == test_note.content
    
    async def test_update_note(self, db, test_note):
        """测试更新笔记"""
        update_data = {
            "title": "更新后的笔记标题",
            "content": "更新后的笔记内容"
        }
        note_update = NoteUpdate(**update_data)
        updated_note = await update_note(db, test_note.id, note_update)
        
        assert updated_note is not None
        assert updated_note.id == test_note.id
        assert updated_note.title == update_data["title"]
        assert updated_note.content == update_data["content"]
        
        # 验证数据库中确实更新了
        db_note = await get_note(db, test_note.id)
        assert db_note.title == update_data["title"]
        assert db_note.content == update_data["content"]
    
    async def test_delete_note(self, db, test_note):
        """测试删除笔记"""
        result = await delete_note(db, test_note.id)
        assert result is True
        
        # 验证已删除
        note = await get_note(db, test_note.id)
        assert note is None
    
    async def test_get_notes_by_user(self, db):
        """测试获取用户所有笔记"""
        # 创建多个笔记
        notes_data = [
            {"title": "用户笔记1", "content": "内容1", "user_id": "test_user"},
            {"title": "用户笔记2", "content": "内容2", "user_id": "test_user"},
            {"title": "用户笔记3", "content": "内容3", "user_id": "test_user"}
        ]
        
        for note_data in notes_data:
            note_in = NoteCreate(**note_data)
            await create_note(db, note_in)
        
        # 测试获取笔记列表
        notes = await get_notes_by_user(db, "test_user")
        
        assert len(notes) == 3
        assert all(note.user_id == "test_user" for note in notes)
        
        # 清理
        await db.notes.delete_many({"user_id": "test_user"}) 