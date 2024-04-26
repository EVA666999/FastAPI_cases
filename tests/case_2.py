from fastapi import FastAPI
from pydantic import BaseModel, constr
from databases import Database

app = FastAPI()

fake_db = [{'username': 'admin', 'password': '123456'}]

class User(BaseModel):
    username: str
    password: constr(min_length=6, max_length=16)

@app.post('/user')
async def create_user(user: User):
    return user

@app.get('/user/{username}', response_model=User)
async def get_user(username: str):
    for user in fake_db:
        if user['username'] == username:
            return user
        else:
            return {"message": "User not found"}
    
@app.delete('/user/{username}')
async def del_user(username):
    for idx, user in enumerate(fake_db):
        if user['username'] == username:
            del fake_db[idx]
            return {"message": "User deleted successfully"}