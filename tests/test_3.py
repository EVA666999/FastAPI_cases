from fastapi.testclient import TestClient
from case_3 import app
import pytest

client = TestClient(app)

def test_for_post_user():
    response = client.post("/users", json={"username": "admin", "password": "123456"})
    assert response.status_code == 200
    assert response.json() == {"username": "admin", "password": "123456"}


def test_for_get_user():
    response = client.get("/users/admin")
    assert response.status_code == 200
    assert response.json() == {"username": "admin", "password": "123456"}

def test_for_put_user():
    response = client.put("/users/admin", json={"username": "admin1", "password": "1234562"})
    assert response.status_code == 200
    assert response.json() == {"message": "User change successfully"}