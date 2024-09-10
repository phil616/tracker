from tortoise import fields
from model.AbstractBase import TimestampMixin
class UserRole(TimestampMixin):
    user_id = fields.IntField(description="User ID",unique=True)
    role = fields.CharField(max_length=255,description="User to Roles, f <role>,<...>")
    class Meta:
        table = "roles"
        table_description = "User to Roles"