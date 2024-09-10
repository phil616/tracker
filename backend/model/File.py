from model.AbstractBase import TimestampMixin
from tortoise import fields

class File(TimestampMixin):
    file_id = fields.IntField(pk=True)
    file_name = fields.CharField(max_length=255, description="Name of the file")
    file_path = fields.CharField(max_length=255, description="Path of the file on the server")
    file_mime_type = fields.CharField(max_length=255, null=True,description="MIME type of the file")
    file_hash = fields.CharField(max_length=255, null=True, description="Hash of the file")

    class Meta:
        table = "files"
        table_description = "Table to store information about files"
