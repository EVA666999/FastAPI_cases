from fastapi import FastAPI, HTTPException
from app.models.models import Todo, tasks
from fastapi.encoders import jsonable_encoder
import psycopg2
from psycopg2 import Error
import mysql.connector

app = FastAPI()

db_params = {
    "host": "localhost",
    "user": "root",
    "password": "vasea01",
    "database": "my_database",
    "port": "3306"  
}


@app.post('/item')
def create(task: Todo):
    try:
        connection = mysql.connector.connect(**db_params)
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO todo (title, description, completed) 
            VALUES (%s, %s, %s) 
            """,
            (task.title, task.description, task.completed)
        )
        connection.commit()

        inserted_task_id = cursor.lastrowid

        cursor.close()
        connection.close()

        return {"id": inserted_task_id, **task.dict()}

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")

@app.get('/item/{id}')
def get_id(id: int, task: Todo):
    try:
        connection = mysql.connector.connect(**db_params)
        cursor = connection.cursor()

        cursor.execute('SELECT id FROM todo WHERE id=%s', (id,))
        
        cursor.fetchone()
        
        connection.commit()

        inserted_task_id = cursor.lastrowid

        cursor.close()
        connection.close()

        return {"id": inserted_task_id, **task.dict()}

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    

@app.patch("/item/{id}", response_model=Todo)
async def update_item(id: int, task_data: dict):
    try:
        connection = mysql.connector.connect(**db_params)
        cursor = connection.cursor()

        cursor.execute('''UPDATE todo
                          SET title = %s,
                              description = %s,
                              completed = %s
                          WHERE id = %s''', 
                       (task_data.get('title'), task_data.get('description'), task_data.get('completed'), id))

        connection.commit()

        inserted_task_id = id

        cursor.close()
        connection.close()

        return {"id": inserted_task_id, **task_data}

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    
@app.delete("/item/{id}")
async def update_item(id: int, task: Todo):
    try:
        connection = mysql.connector.connect(**db_params)
        cursor = connection.cursor()
        cursor.execute('''DELETE FROM todo
                          WHERE id=%s''', (id,))
        cursor.fetchone()
            
        connection.commit()

        connection.commit()

        cursor.close()
        connection.close()

        return {"message": "Запись удалена!"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")