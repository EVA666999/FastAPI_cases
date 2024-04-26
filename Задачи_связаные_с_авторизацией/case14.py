import jwt
from fastapi import FastAPI, HTTPException, Depends, status
from app.models.models import Userjwt1, users_db1
from fastapi.security import OAuth2PasswordBearer
import requests
from fastapi.encoders import jsonable_encoder


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

def get_user(username: str):
    for user_data in users_db1:
        if user_data["username"] == username:
            print("Found user:", user_data)  # Отладочное сообщение
            return Userjwt1(**user_data)
    print("User not found for username:", username)  # Отладочное сообщение
    return None




def create_jwt_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


@app.post('/register')
async def register(user: Userjwt1):
    user_data = user.model_dump()
    users_db1.append(user_data)
    print("User registered:", user_data)  # Добавляем отладочный вывод
    return user

@app.post("/login")
async def login(user_in: Userjwt1):
    for user in users_db1:
        user_dict = user
        if user_dict["username"] == user_in.username and user_dict["password"] == user_in.password:
            return {"access_token": create_jwt_token({"sub": user_in.username}), "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Функция получения User'а по токену
@app.get("/protected_resource")
def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # декодируем токен
        print("Payload:", payload)  # Добавляем отладочный вывод
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        return {'message': 'токен истёк'}
    except jwt.InvalidTokenError:
        return {'message': 'неправильный токен'}

# Защищенный роут для админов, когда токен уже получен
@app.get("/admin")
def get_admin_info(current_user: str = Depends(get_user_from_token)):
    print("Current user:", current_user)  # Добавляем отладочный вывод
    user_data = get_user(current_user)
    print("User data:", user_data)  # Добавляем отладочный вывод
    if user_data is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is None")
    if user_data.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return {"message": "Welcome Admin!"}

@app.patch("/users/{username}", response_model=Userjwt1)
async def update_item(username: str, user: Userjwt1, current_user: str = Depends(get_user_from_token)):
    user_data = get_user(current_user)
    if user_data.role == "admin" or user_data.role == 'user':
        for stored_user in users_db1:
            if stored_user["username"] == username:
                stored_user_model = Userjwt1(**stored_user)
                update_data = user.model_dump(exclude_unset=True)
                updated_user = stored_user_model.model_copy(update=update_data)
                index = users_db1.index(stored_user)
                users_db1[index] = jsonable_encoder(updated_user)
                return updated_user
        raise HTTPException(status_code=404, detail="User not found")
    
@app.get("/users/{username}", response_model=Userjwt1)
async def update_item(current_user: str = Depends(get_user_from_token)):
    user_data = get_user(current_user)
    if user_data.role == "guest":
        return user_data
    raise HTTPException(status_code=404, detail="User not found")