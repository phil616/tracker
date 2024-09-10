from model.AbstractBase import TimestampMixin
from tortoise import fields
from pydantic import BaseModel
from datetime import datetime
class Task(TimestampMixin):
    task_id = fields.IntField(pk=True)
    task_start_time = fields.DatetimeField(null=True,description="Task start time")
    task_status = fields.IntField(default=0,description="0-Not Planned, 1-Pending, 2-Noticed, 3-Completed, 4-Cancelled")
    task_name = fields.CharField(max_length=255)
    task_description = fields.CharField(max_length=255,null=True)
    task_priority = fields.IntField(default=1,null=True,description="1-High, 2-Medium, 3-Low")
    task_assignee = fields.IntField()
    class Meta:
        table = "task"
        table_description = "This table is used to store all the tasks"

class TaskResponse(BaseModel):
    task_id: int
    task_start_time: datetime
    task_status: int
    task_name: str
    task_description: str = None
    task_priority: int
    task_assignee: int

class TaskSchema(BaseModel):
    task_start_time: datetime
    task_status: int = 0
    task_name: str
    task_description: str = None
    task_priority: int = 1
    task_assignee: int

