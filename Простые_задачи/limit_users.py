from fastapi import FastAPI

app = FastAPI()

# Пример пользовательских данных (для демонстрационных целей) 
fake_users = {
    1: {"username": "john_doe", "email": "john@example.com"},
    2: {"username": "jane_smith", "email": "jane@example.com"},
}

@app.get("/users/")
def read_users(limit: int = 10):
    return dict(list(fake_users.items())[:limit])