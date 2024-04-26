from typing import Optional, Union
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, conint, constr

app = FastAPI()

class User(BaseModel):
    username: str
    age: conint(gt=18)
    email: EmailStr
    password: constr(min_length=8, max_length=16)
    phone: Optional[str] = 'Unknown'

@app.exception_handler(HTTPException)  # обработчик для HTTPException
async def http_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})

@app.post("/user")
async def create_user(user: User):
    try:
        if user.username == 'admin':
            raise HTTPException("invalid username! User cant be admin!")
        elif user.age > 100:
            raise HTTPException(status_code=400, detail="age must be < 100")
        elif user.email == 'admin@mail.com':
            raise HTTPException(status_code=400, detail="Invalid Email!")
        return {"message": "Item created successfully", "user": user}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))