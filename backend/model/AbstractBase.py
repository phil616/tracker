from tortoise import Model, fields

class TimestampMixin(Model):
    created_at = fields.DatetimeField(auto_now_add=True, description="Created at")
    updated_at = fields.DatetimeField(auto_now=True, description="Updated at")
    created_by = fields.CharField(default="[SYSTEM]",max_length=255, null=True, description="Created by")
    updated_by = fields.CharField(default="[SYSTEM]",max_length=255, null=True, description="Updated by")

    class Meta:
        abstract = True