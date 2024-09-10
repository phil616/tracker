from response.std import URFRouter
from model.Task import Task,TaskSchema,TaskResponse
from datetime import datetime
from typing import Union
task_router = URFRouter(prefix="/task")

@task_router.get("/all")
async def get_all_tasks()->list[TaskResponse]:
    tasks =  await Task.all()
    response_tasks = []
    for task in tasks:
        response_tasks.append(TaskResponse(**task.__dict__))
    return response_tasks

@task_router.post("/new/task")
async def create_new_task(task:TaskSchema):
    return await Task.create(**task.model_dump())

@task_router.get("/taskByID")
async def get_task_by_id(id:int)->Union[TaskResponse,dict]:
    task = await Task.filter(task_id=id).first()
    if task:
        return TaskResponse(**task.__dict__)
    else:
        return {"message": "Task not found"}

@task_router.put("/update/task")
async def update_task(id:int, task:TaskSchema):
    task_obj = await Task.filter(task_id=id).first()
    task_obj.update_from_dict(task.model_dump())
    await task_obj.save()
    return task_obj

@task_router.delete("/delete/task")
async def delete_task(id:int):
    task_obj = await Task.filter(task_id=id).first()
    await task_obj.delete()
    return {"message": "Task deleted successfully"}

@task_router.get("/taskByDate")
async def get_task_by_date(date_start:datetime, date_end:datetime) -> list[TaskResponse]:
    all_tasks = await Task.all()
    tasks_by_date = []
    for task in all_tasks:
        if date_start <= task.created_at <= date_end:
            tasks_by_date.append(TaskResponse(**task.__dict__))

    return tasks_by_date


