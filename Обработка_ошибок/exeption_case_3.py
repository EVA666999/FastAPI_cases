from fastapi import FastAPI, HTTPException, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import time


app = FastAPI()

class ErrorResponseModel(BaseModel):
    status_code: int
    message: str
    error_code: str = None

class User(BaseModel):
    username: str
    age: int
users = []

class UserNotFoundException(HTTPException):
    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)

class InvalidUserDataException(HTTPException):
    def __init__(self, message: str, headers: dict = None):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = message
        self.headers = headers or {}


@app.exception_handler(UserNotFoundException)
async def http_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})

@app.exception_handler(InvalidUserDataException)
async def http_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail},  headers=exc.headers)


@app.post('/register', status_code=201)
async def register(user: User, response: Response):
    if user.username == 'admin':
            start_time = time.time()
            raise InvalidUserDataException("invalid username! User cant be admin!")
    else:
        users.append(user)
        response.status_code = status.HTTP_201_CREATED
        print(users)
        return user

@app.get('/user/{username}')
async def get_user(username):
        for user in users:
            print(users)
            if user.username == username:
                return user
        raise UserNotFoundException("User not found!")
