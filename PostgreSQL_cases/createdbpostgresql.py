from fastapi import FastAPI, HTTPException
from databases import Database
from typing import Optional
from app.models.models import Todo

app = FastAPI()

DATABASE_URL = "postgresql://postgres:vasea01@localhost/postgres"

database = Database(DATABASE_URL)

@app.on_event("startup")
async def startup_database():
    await database.connect()

@app.on_event("shutdown")
async def shutdown_database():
    await database.disconnect()

@app.post("/task", response_model=Todo)
async def create_task(task: Todo):
    query = "INSERT INTO todo (title, description, completed) VALUES (:title, :description, :completed) RETURNING id"
    values = {"title": task.title, "description": task.description, "completed": task.completed}
    try:
        task_id = await database.execute(query=query, values=values)
        return {**task.dict(), "id": task_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create task")
    
@app.get("/task/{task_id}", response_model=Todo)
async def get_task(task_id: int):
    query = "SELECT * FROM todo WHERE id = :task_id"
    values = {"task_id": task_id}
    try:
        result = await database.fetch_one(query=query, values=values)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch task from database")

    if result is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_data = dict(result)
    return Todo(**task_data)


@app.put("/task/{task_id}", response_model=Todo)
async def update_task(task_id: int, task: Todo):
    query = "UPDATE todo SET title = :title, description = :description, completed = :completed WHERE id = :task_id"
    values = {"task_id": task_id, "title": task.title, "description": task.description, "completed": task.completed}
    try:
        await database.execute(query=query, values=values)
        return {**task.dict(), "id": task_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to update task in database")
    

@app.delete("/task/{task_id}", response_model=dict)
async def delete_task(task_id: int):
    query = "DELETE FROM todo WHERE id = :task_id RETURNING id"
    values = {"task_id": task_id}
    try:
        deleted_rows = await database.execute(query=query, values=values)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to delete task from database")
    if deleted_rows:
        return {"message": "task deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="task not found")