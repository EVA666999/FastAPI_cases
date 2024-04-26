from fastapi.testclient import TestClient
from case_2 import app
import pytest

client = TestClient(app)

def test_for_post_user():
    response = client.post("/user", json={"username": "admin", "password": "123456"})
    assert response.status_code == 200
    assert response.json() == {"username": "admin", "password": "123456"}


def test_for_get_user():
    response = client.get("/user/admin")
    assert response.status_code == 200
    assert response.json() == {"username": "admin", "password": "123456"}

def test_for_delete_user():
    response = client.delete("/user/admin")
    assert response.status_code == 200
    assert response.json() == {"message": "User deleted successfully"}


@pytest.fixture
def test_client():
    return TestClient(app)

def test_create_user(test_client):
    response = test_client.post("/user", json={"username": "test_user", "password": "test123456"})
    assert response.status_code == 200
    assert response.json() == {"username": "test_user", "password": "test123456"}