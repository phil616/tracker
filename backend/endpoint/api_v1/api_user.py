# user management TODO: impl
# account [login] [logout] [register] [forgot password] [reset password] [update profile] [delete account]
# manage user roles [create user] [edit user] [delete user] [assign role] [revoke role] [view user roles]

from response.std import URFRouter
from fastapi import Security
from core.authorize import check_permissions
user_router = URFRouter(prefix="/user", dependencies=[Security(check_permissions, scopes=["user:read", "user:write"])])

@user_router.get("/info")
def get_user_info(request):
    return {"message": "User info"}


@user_router.post("/passwordReset")
async def reset_password(request):
    return {"message": "Password reset"}


@user_router.post("/passwordForgot")
async def forgot_password(request):
    return {"message": "Password forgot"}

