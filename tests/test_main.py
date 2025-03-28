import pytest

@pytest.mark.asyncio
async def test_read_root(test_client):
    response = await test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to ThoughtGrove API"} 