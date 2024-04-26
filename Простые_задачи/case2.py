from fastapi import FastAPI

app1 = FastAPI()

@app1.post('/calculate/{num1}/{num2}')
async def calculate(num1: int, num2: int):
    result = num1 + num2
    return {"result": result}

app1.get()
