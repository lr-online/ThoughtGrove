import pytest
from pydantic import ValidationError
from thoughtgrove.models.user import UserCreate, UserUpdate

def test_user_create_valid():
    user = UserCreate(
        email="test@example.com",
        username="testuser",
        password="Test123456"
    )
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.password == "Test123456"
    assert user.is_active is True
    assert user.is_superuser is False

def test_user_create_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(
            email="invalid-email",
            username="testuser",
            password="Test123456"
        )

def test_user_create_invalid_username():
    with pytest.raises(ValidationError):
        UserCreate(
            email="test@example.com",
            username="te",  # too short
            password="Test123456"
        )

def test_user_create_invalid_password():
    with pytest.raises(ValidationError):
        UserCreate(
            email="test@example.com",
            username="testuser",
            password="weak"  # too weak
        )

def test_user_update_valid():
    user = UserUpdate(
        email="new@example.com",
        username="newuser",
        password="NewTest123456"
    )
    assert user.email == "new@example.com"
    assert user.username == "newuser"
    assert user.password == "NewTest123456"

def test_user_update_partial():
    user = UserUpdate(email="new@example.com")
    assert user.email == "new@example.com"
    assert user.username is None
    assert user.password is None 