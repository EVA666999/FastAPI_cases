from app.models.models import Authorizate, authorizate_users
from fastapi import FastAPI, Cookie, Response, Depends
from datetime import datetime
from fastapi.security import APIKeyCookie
import random
import string

cookie_scheme = APIKeyCookie(name="session_token")

app = FastAPI()

@app.post('/login')
async def login(user: Authorizate, response: Response):
    authorizate_users.append(user)
    N = 11
    key = ''.join(random.choices(string.ascii_uppercase +
                        string.digits, k=N))
    response.set_cookie(key="session_token", value=key)
    return  {'session_token': key}


@app.get('/user')
async def auth_user(session_token = Cookie()):
    return {'session_token': session_token}

@app.post('/user')
async def post_auth_user(user: Authorizate, session_token = Cookie()):
    if user.session_token == session_token:
        return user
    else: 
        return {"message": "Unauthorized"}