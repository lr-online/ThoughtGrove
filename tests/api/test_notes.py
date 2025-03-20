import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from thoughtgrove.main import app
from thoughtgrove.models.note import NoteCreate


@pytest.fixture
def note_data():
    return {
        "title": "测试笔记标题",
        "content": "这是一篇测试笔记的内容"
    }


class TestNotesAPI:
    async def test_create_note(self, async_client: AsyncClient, token_header, note_data):
        """测试创建笔记API"""
        response = await async_client.post(
            "/api/notes/", 
            json=note_data,
            headers=token_header
        )
        
        # 打印详细错误信息便于调试
        if response.status_code != 201:
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == note_data["title"]
        assert data["content"] == note_data["content"]
        assert "id" in data
        # 删除创建的笔记，避免影响其他测试
        await async_client.delete(f"/api/notes/{data['id']}", headers=token_header)
    
    async def test_read_note(self, async_client: AsyncClient, token_header, note_data, db):
        """测试读取笔记API"""
        # 先创建一个笔记
        create_response = await async_client.post(
            "/api/notes/", 
            json=note_data,
            headers=token_header
        )
        create_data = create_response.json()
        note_id = create_data["id"]
        
        # 测试读取笔记
        response = await async_client.get(
            f"/api/notes/{note_id}",
            headers=token_header
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == note_id
        assert data["title"] == note_data["title"]
        assert data["content"] == note_data["content"]
        
        # 清理
        await async_client.delete(f"/api/notes/{note_id}", headers=token_header)
    
    async def test_update_note(self, async_client: AsyncClient, token_header, note_data):
        """测试更新笔记API"""
        # 先创建一个笔记
        create_response = await async_client.post(
            "/api/notes/", 
            json=note_data,
            headers=token_header
        )
        create_data = create_response.json()
        note_id = create_data["id"]
        
        # 更新数据
        update_data = {
            "title": "更新后的标题",
            "content": "更新后的内容"
        }
        
        # 测试更新笔记
        response = await async_client.put(
            f"/api/notes/{note_id}",
            json=update_data,
            headers=token_header
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == note_id
        assert data["title"] == update_data["title"]
        assert data["content"] == update_data["content"]
        
        # 清理
        await async_client.delete(f"/api/notes/{note_id}", headers=token_header)
    
    async def test_delete_note(self, async_client: AsyncClient, token_header, note_data):
        """测试删除笔记API"""
        # 先创建一个笔记
        create_response = await async_client.post(
            "/api/notes/", 
            json=note_data,
            headers=token_header
        )
        create_data = create_response.json()
        note_id = create_data["id"]
        
        # 测试删除笔记
        response = await async_client.delete(
            f"/api/notes/{note_id}",
            headers=token_header
        )
        
        assert response.status_code == 204
        
        # 验证确实已删除
        get_response = await async_client.get(
            f"/api/notes/{note_id}",
            headers=token_header
        )
        assert get_response.status_code == 404
    
    async def test_read_user_notes(self, async_client: AsyncClient, token_header, db):
        """测试读取用户所有笔记API"""
        # 创建多个笔记
        notes_data = [
            {"title": "用户笔记1", "content": "内容1"},
            {"title": "用户笔记2", "content": "内容2"},
            {"title": "用户笔记3", "content": "内容3"}
        ]
        
        created_note_ids = []
        for note_data in notes_data:
            response = await async_client.post(
                "/api/notes/", 
                json=note_data,
                headers=token_header
            )
            data = response.json()
            created_note_ids.append(data["id"])
        
        # 测试获取笔记列表
        response = await async_client.get(
            "/api/notes/",
            headers=token_header
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3  # 至少包含我们创建的3个笔记
        
        # 清理创建的笔记
        for note_id in created_note_ids:
            await async_client.delete(f"/api/notes/{note_id}", headers=token_header)
    
    async def test_create_note_validation(self, async_client: AsyncClient, token_header):
        """测试创建笔记的数据验证"""
        # 标题为空
        invalid_data = {"title": "", "content": "内容"}
        response = await async_client.post(
            "/api/notes/", 
            json=invalid_data,
            headers=token_header
        )
        assert response.status_code == 422
        
        # 内容为空
        invalid_data = {"title": "标题", "content": ""}
        response = await async_client.post(
            "/api/notes/", 
            json=invalid_data,
            headers=token_header
        )
        assert response.status_code == 422 