from fastapi import FastAPI
from app.models.models import Feedback, users

app = FastAPI()

@app.get("/users")
async def get_users():
    return users

@app.post('/send_message')
async def send_message(user: Feedback):
    users.append(user)
    return {"message": "Feedback received. Thank you, Alice!"}