from datetime import datetime, date
from typing import List, Optional, Union
from pydantic import EmailStr
from pydantic import Field

from pydantic import BaseModel

class User(BaseModel):
    name: str
    id: int

class Userjwt(BaseModel):
    username: str
    password: str
users_db = []

class Userjwt1(BaseModel):
    username: str
    password: str
    role: Optional[str] = None
users_db1 = []

class Todo(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    completed: bool = False
tasks = []

class User1(BaseModel):
    name: str
    age: int
    is_adult: bool = False

class Feedback(BaseModel):
    name: str
    message: str
users = []

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int
    is_sub: bool = False

class Products(BaseModel):
    product_id: int
    name: str
    category: str
    price: int
product_list = []

class Product(BaseModel):
    id: int
    title: str
    price: int
    count: int

class Authorizate(BaseModel):
    username: str
    password: str
    session_token: str = None
authorizate_users = []