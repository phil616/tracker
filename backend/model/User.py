from tortoise import fields
from model.AbstractBase import TimestampMixin
from pydantic import BaseModel
class User(TimestampMixin):
    user_id = fields.IntField(pk=True,description="User ID")
    username = fields.CharField(max_length=255,unique=True,description="Username")
    password = fields.CharField(max_length=255,description="Password")   
    email = fields.CharField(max_length=255,null=True,unique=True, description="Email")
    is_active = fields.BooleanField(default=True,description="Is Active")

    class Meta:
        table = "users"
        description = "User Table"


class UserRegisterSchema(BaseModel):
    username: str
    password: str
    email: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "password": "password123",
                "email": "johndoe@example.com"
            }
        }