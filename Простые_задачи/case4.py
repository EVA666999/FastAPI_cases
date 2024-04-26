from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class User(BaseModel):
    username: str
    message: str
    
@app.post("/")
async def root(user: User):
    print(f'Мы получили от юзера {user.username} такое сообщение: {user.message}') 
    return user