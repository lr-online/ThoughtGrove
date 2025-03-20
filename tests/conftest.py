import os
import pytest
from datetime import timedelta
from httpx import AsyncClient
from thoughtgrove.main import app
from thoughtgrove.db.mongodb import mongodb
from thoughtgrove.core.security import create_access_token
from thoughtgrove.models.user import UserCreate
from thoughtgrove.crud.user import create_user

# 使用应用默认环境变量配置

@pytest.fixture
async def test_client():
    """创建测试客户端"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
async def async_client():
    """创建异步测试客户端"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
def db():
    """返回数据库实例"""
    return mongodb.db

@pytest.fixture(autouse=True)
async def setup_db():
    """设置测试数据库"""
    # 连接数据库
    await mongodb.connect()
    
    # 清理集合
    db = mongodb.db
    await db.users.delete_many({})
    await db.notes.delete_many({})
    
    yield
    
    # 清理数据并关闭连接
    await db.users.delete_many({})
    await db.notes.delete_many({})
    await mongodb.close()

@pytest.fixture
async def test_user(db):
    """创建测试用户"""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "Password123",  # 符合密码强度要求：大小写字母和数字
    }
    user_in = UserCreate(**user_data)
    user = await create_user(user_in)
    return user

@pytest.fixture
async def token_header(test_user):
    """创建认证头"""
    # 创建访问令牌
    access_token = create_access_token(
        data={"sub": test_user.email},
        expires_delta=timedelta(minutes=30)
    )
    return {"Authorization": f"Bearer {access_token}"} 