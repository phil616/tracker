from tortoise import fields
from model.AbstractBase import TimestampMixin
class RoleScope(TimestampMixin):
    role = fields.CharField(max_length=255, description="Role of the user in the system")
    scopes = fields.CharField(max_length=255, description="List of scopes. f<scope>,<...>")

    class Meta:
        table = "scopes"
        table_description = "Table to store the scopes of the users"