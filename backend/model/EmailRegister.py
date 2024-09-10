from tortoise import fields
from model.AbstractBase import TimestampMixin

class EmailRegister(TimestampMixin):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255)
    hex_key = fields.CharField(max_length=255, unique=True)
    
    class Meta:
        table = "email_register"
        table_description = "Email Register Table"
