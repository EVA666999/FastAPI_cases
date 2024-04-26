from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()


# класс кастомного исключения для ошибок
class CustomException(HTTPException):
    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


# пример маршрута, который райзит (выбрасывает) кастомное исключение 
@app.get("/items/{item_id}/")
async def read_item(item_id: int):
    if item_id == 42:
        raise CustomException(detail="Item not found", status_code=404)
    return {"item_id": item_id}

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()


# не изменяли
class CustomException(HTTPException):
    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


# Обработчик ошибок (error handler) для класса CustomException 
@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )


from pydantic import BaseModel

# Pydantic модель ответов на ошибки
class ErrorResponse(BaseModel):
    error_code: int
    error_message: str
    error_details: str = None