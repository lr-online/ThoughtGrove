import os
import pytest
from httpx import AsyncClient
from thoughtgrove.main import app
from thoughtgrove.db.mongodb import mongodb

# 使用应用默认环境变量配置

@pytest.fixture
async def test_client():
    """创建测试客户端"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture(autouse=True)
async def setup_db():
    """设置测试数据库"""
    # 连接数据库
    await mongodb.connect()
    
    # 清理集合
    db = mongodb.db
    await db.users.delete_many({})
    
    yield
    
    # 清理数据并关闭连接
    await db.users.delete_many({})
    await mongodb.close() 