from response.std import URFRouter
from fastapi import Security
from core.authorize import check_permissions
user_manage_router = URFRouter(prefix="/userManage", dependencies=[Security(check_permissions,  scopes=["user:read", "user:write","user:delete","user:create"])])

...
