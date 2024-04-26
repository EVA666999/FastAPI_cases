from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.models.models import User

app = FastAPI()

class ErrorResponse(BaseModel):
    error_code: int
    error_message: str
    error_details: str = None
    
# класс кастомного исключения для ошибок
class CustomExceptionA(HTTPException):
    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)

class CustomExceptionB(HTTPException):
    def __init__(self, detail: str, status_code: int = 404):
        super().__init__(status_code=status_code, detail=detail)

@app.exception_handler(CustomExceptionA)
async def custom_exception_handler(request: Request, exc: CustomExceptionA):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error_not_right": exc.detail}
    )

@app.exception_handler(CustomExceptionB)
async def custom_exception_handler(request: Request, exc: CustomExceptionB):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error_not_found": exc.detail}
    )


@app.get("/calculate/{num1}/{num2}")
async def read_item(num1: int, num2: int):
    result = num1 + num2
    if result == 4:
        return result
    else:
        raise CustomExceptionA(detail="sum of numbers != 4", status_code=404)
    
@app.get("/items/{item_id}/")
async def read_item(item_id: int):
    if item_id != 42:
        raise CustomExceptionB(detail="Item not found", status_code=404)
    return {"item_id": item_id}
    