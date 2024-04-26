from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, constr
from databases import Database

app = FastAPI()

# URL для PostgreSQL (измените его под свою БД)
DATABASE_URL = "postgresql://postgres:vasea01@localhost/postgres"

database = Database(DATABASE_URL)

@app.on_event("startup")
async def startup_database():
    await database.connect()

@app.on_event("shutdown")
async def shutdown_database():
    await database.disconnect()
    

class User(BaseModel):
    username: str
    password: constr(min_length=6, max_length=16)

fake_db = [{'username': 'olajda', 'password': '12345767'}]

# создание роута для создания юзеров
@app.post("/users", response_model=User)
async def create_user(user: User):
    query = "INSERT INTO users (username, password) VALUES (:username, :password)"
    values = {"username": user.username, "password": user.password}
    try:
        await database.execute(query=query, values=values)
        return user
    except Exception as e:
        print(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Failed to create user")


@app.get("/users/{username}", response_model=User)
async def get_user(username: str):
    query = "SELECT * FROM users WHERE username = :username"
    values = {"username": username}
    try:
        result = await database.fetch_one(query=query, values=values)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch user from database")

    if result is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Создаем экземпляр UserReturn на основе данных из базы данных
    user_data = dict(result)
    return User(**user_data)


@app.put("/users/{username}", response_model=User)
async def update_user(username: str, new_user: User):
    query = "UPDATE users SET username = :new_username, password = :password WHERE username = :old_username"
    values = {"new_username": new_user.username, "password": new_user.password, "old_username": username}
    try:
        await database.execute(query=query, values=values)
        return {**new_user.dict(), "username": new_user.username}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to update user in database")
