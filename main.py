from typing import Union

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from pydantic import BaseModel

from tasks import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # Change in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

task_storage = TaskRepository()

class DeterminantAnswerSchema(BaseModel):
    value: int

class SLAUAnswerSchema(BaseModel):
    value: list

AnswerUnion = Union[DeterminantAnswerSchema, SLAUAnswerSchema]

@app.get("/ping")
def ping():
    return {"ok" : True}


# Tasks
@app.post("/tasks/determinant", tags=["Users"], summary="Получить задание по решению определителя")
def send_determinant(matrix_width:int=3, matrix_height:int=3):
    matrix = np.random.randint(-10, 10, (matrix_width, matrix_height))
    task = DeterminantTask(matrix)
    task_storage.save(task)
    return {"task_id": task.id, "question": task.get_question()}

@app.post("/tasks/slau", tags=["Users"], summary="Получить задание по решению СЛАУ")
def send_slau(variables: int = 3):
    while True:
        coefficients = np.random.randint(-10, 10, (variables, variables))
        biases = np.random.randint(-10, 10, (variables, 1))
        try:
            task = SLAUTask(coefficients, biases)
            break
        except np.linalg.LinAlgError:
            pass
    task_storage.save(task)
    return {"task_uuid": task.id, "question": task.get_question()}


# Answers
@app.post("/answers/{task_uuid}", summary="Проверить правильность ответа")
def check_answer(task_uuid: str, answer: AnswerUnion):
    task = task_storage.find_by_id(task_uuid)
    if not task:
        raise HTTPException(status_code=404, detail="Task with the given uuid was not found.")
    solution = task.get_answer()
    if type(solution) != type(answer.value):
        raise HTTPException(status_code=415, detail="Incorrect data type in answer field.")

    if solution == answer.value:
        return {"ok" : True}
    return {"ok" : False}

@app.get("/answers/{task_uuid}", summary="Получить верный ответ", tags=["Admin"])
def get_true_answer(task_uuid: str):
    task = task_storage.find_by_id(task_uuid)
    if not task:
        raise HTTPException(status_code=404, detail="Task with the given uuid was not found.")
    solution = task.get_answer()
    return {"answer" : solution}
    

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)