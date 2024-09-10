from model.UserRole import UserRole
from model.RoleScope import RoleScope
from model.User import User
from core.setting import config
from core.authorize import role_scopes
from database.sqlite import get_sqlite_db_config
from core.logger import log
from tortoise import Tortoise
from lib.hash import hash_util 
from core.background import bg_check_tasks
from fastapi import BackgroundTasks
import asyncio
async def setup():

    await Tortoise.init(get_sqlite_db_config())
    await Tortoise.generate_schemas()
    log.info("database connected")


    # init RoleScope
    db_role_scopes = await RoleScope.all()
    for db_role_scope in db_role_scopes:
        await db_role_scope.delete()
    system_roles = role_scopes.keys()
    for role in system_roles:
        await RoleScope.create(role=role, scopes=",".join(role_scopes[role]))
    
    # init super user
    super_user = await User.filter(username=config.SUPERUSER)
    if not super_user:
        hashed_password = hash_util.bcrypt(config.SUPERPASS)
        s_user = await User.create(username=config.SUPERUSER, password=hashed_password,email=config.SUPEREMAIL)
        await UserRole.update_or_create(user_id=s_user.user_id,role=",".join(role_scopes.keys()))
    

    # background task
    asyncio.create_task(bg_check_tasks())

    log.info("application initialized")

async def teardown():
    await Tortoise.close_connections()

    log.info("database disconnected")

    
    log.info("application terminated")