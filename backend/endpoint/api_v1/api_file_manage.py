from response.std import URFRouter
from model.File import File
from fastapi import Security
from core.authorize import check_permissions

file_urf_router = URFRouter(prefix="/fileManage",dependencies=[Security(check_permissions, scopes=["system:read","system:write"])])


@file_urf_router.get("/list")
async def file_manage_list():
    files = await File.all()
    return files
