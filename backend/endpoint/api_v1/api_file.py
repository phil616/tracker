from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from model.File import File as FileModel
from aiofiles import open as aio_open
from core.utils import get_random_string, get_bytes_hash
from os import path
from fastapi import Security
from core.authorize import check_permissions

async def save_file(file: bytes, file_name: str):
    async with aio_open(file_name, "wb") as f:
        await f.write(file)


async def get_file(file_name: str)->bytes:
    async with aio_open(file_name, "rb") as f:
        contents = await f.read()
        return contents

file_router = APIRouter(prefix="/file",dependencies=[Security(check_permissions, scopes=["user:read", "user:write"])])

@file_router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    hash_value = get_bytes_hash(contents)
    exists_file = await FileModel.filter(file_hash=hash_value).first()
    await FileModel.create(
        file_name=exists_file.file_name,
        file_mime_type=exists_file.file_mime_type,
        file_path=exists_file.file_path,
        file_hash=exists_file.file_hash
    )
    if exists_file:
        return {"message": "File already exists", "file_id": exists_file.file_id}
    
    file_disk_name = get_random_string(24) + ".appfile"
    
    await save_file(contents, path.join("storage", file_disk_name))
    new_file = await FileModel.create(
        file_name=file.filename,
        file_mime_type=file.content_type,
        file_path=file_disk_name,
        file_hash=hash_value
    )
    return {"message": "File uploaded successfully", "file_id": new_file.file_id}

@file_router.get("/download/{file_id}")
async def get_file_by_id(file_id: int):
    file = await FileModel.filter(file_id=file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=path.join("storage", file.file_path), filename=file.file_name)

