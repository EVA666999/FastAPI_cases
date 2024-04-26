from app.models.models import User, User1



from fastapi import FastAPI


app = FastAPI()


@app.get("/users")
async def root(user: User):
    return user

@app.post('/user')
async def post(user1: User1):
    if user1.age >= 18:
        user1.is_adult = True
        return user1
    else:
        user1.is_adult = False
        return user1