from fastapi import APIRouter
from endpoint.api_v1.api_authorize import authorize_router
from endpoint.api_v1.api_user import user_router
from endpoint.api_v1.api_cache import cache_router
from endpoint.api_v1.api_file import file_router
from endpoint.api_v1.api_file_manage import file_urf_router
from endpoint.api_v1.api_user_manage import user_manage_router
from endpoint.api_v1.api_task_manager import task_router as task_manager_router
from endpoint.api_v1.api_schedule import schedule_router
v1_router = APIRouter(prefix="/api")

v1_router.include_router(authorize_router, tags=["authorize"])
v1_router.include_router(user_router, tags=["user"])
v1_router.include_router(cache_router, tags=["cache"])
v1_router.include_router(file_router, tags=["file"])
v1_router.include_router(file_urf_router, tags=["file_urf"])
v1_router.include_router(user_manage_router, tags=["user_manage"])
v1_router.include_router(task_manager_router, tags=["task_manager"])
v1_router.include_router(schedule_router, tags=["schedule"])