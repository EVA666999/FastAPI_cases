import jwt
from fastapi import FastAPI, HTTPException, Depends
from app.models.models import Userjwt, users_db
from fastapi.security import OAuth2PasswordBearer
import requests

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

@app.post('/register')
async def register(user: Userjwt):
    users_db.append(user.model_dump())
    return user


def create_jwt_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/login")
async def login(user_in: Userjwt):
    for user in users_db:
        user_dict = user
        if user_dict["username"] == user_in.username and user_dict["password"] == user_in.password:
            return {"access_token": create_jwt_token({"sub": user_in.username}), "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/protected_resource")
def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # декодируем токен
        return payload.get("sub"), {"message": "Доступ разрешён"}
    except jwt.ExpiredSignatureError:
        return {'message': 'токен истёк'}
    except jwt.InvalidTokenError:
        return {'message': 'неправильный токен'}