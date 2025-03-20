import asyncio
import os
import pytest
from httpx import AsyncClient
from dotenv import load_dotenv
from thoughtgrove.main import app
from thoughtgrove.db.mongodb import mongodb

# 使用应用默认环境变量配置

@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()

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