from model.AbstractBase import TimestampMixin
from tortoise import fields
from datetime import date
from pydantic import BaseModel
class Schedule(TimestampMixin):
    schedule_id = fields.IntField(pk=True)
    schedule_date = fields.DateField()
    schedule_place = fields.CharField(max_length=255)
    schedule_title = fields.CharField(max_length=255)
    schedule_description = fields.CharField(max_length=255)
    receiver_email = fields.CharField(max_length=255)
    is_sent = fields.BooleanField(default=False)
    class Meta:
        table = "schedule"
        table_description = "This table is used to store the schedules of the events."

class ScheduleIn(BaseModel):
    schedule_date:date
    schedule_place:str
    schedule_title:str
    schedule_description:str
    user_id:int
    class Config:
        orm_mode = True