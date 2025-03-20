import pytest
from fastapi.testclient import TestClient
from thoughtgrove.main import app

@pytest.fixture
def client():
    return TestClient(app) 