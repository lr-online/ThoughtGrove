import pytest
from httpx import AsyncClient

from thoughtgrove.models.user import UserCreate
from thoughtgrove.crud.user import create_user

@pytest.fixture
async def test_user():
    """创建测试用户"""
    user_in = UserCreate(
        email="test@example.com",
        username="testuser",
        password="Test123456"
    )
    return await create_user(user_in)

@pytest.mark.asyncio
async def test_register_success(test_client: AsyncClient):
    """测试用户注册成功"""
    response = await test_client.post(
        "/auth/register",
        json={
            "email": "new@example.com",
            "username": "newuser",
            "password": "Test123456"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "new@example.com"
    assert data["username"] == "newuser"
    assert "password" not in data
    assert "hashed_password" not in data

@pytest.mark.asyncio
async def test_register_duplicate_email(test_client: AsyncClient, test_user):
    """测试注册重复邮箱"""
    response = await test_client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "username": "anotheruser",
            "password": "Test123456"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "该邮箱已被注册"

@pytest.mark.asyncio
async def test_login_success(test_client: AsyncClient, test_user):
    """测试用户登录成功"""
    response = await test_client.post(
        "/auth/login",
        data={
            "username": "test@example.com",
            "password": "Test123456"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_wrong_password(test_client: AsyncClient, test_user):
    """测试登录密码错误"""
    response = await test_client.post(
        "/auth/login",
        data={
            "username": "test@example.com",
            "password": "WrongPassword"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "邮箱或密码错误"

@pytest.mark.asyncio
async def test_login_nonexistent_user(test_client: AsyncClient):
    """测试登录不存在的用户"""
    response = await test_client.post(
        "/auth/login",
        data={
            "username": "nonexistent@example.com",
            "password": "Test123456"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "邮箱或密码错误"

@pytest.mark.asyncio
async def test_get_current_user(test_client: AsyncClient, test_user):
    """测试获取当前用户"""
    # 先登录获取令牌
    login_response = await test_client.post(
        "/auth/login",
        data={
            "username": "test@example.com",
            "password": "Test123456"
        }
    )
    token = login_response.json()["access_token"]
    
    # 使用令牌访问需要认证的接口
    response = await test_client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"

@pytest.mark.asyncio
async def test_get_current_user_invalid_token(test_client: AsyncClient):
    """测试使用无效令牌"""
    response = await test_client.get(
        "/users/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "无效的认证凭据" 