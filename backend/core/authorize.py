## authorize.py 
# OAuth2.0 Password Grant Type Implementation

from typing import Dict, Union
import uuid
from fastapi.security import  SecurityScopes, OAuth2PasswordBearer
from fastapi import Depends, HTTPException, Request
from datetime import datetime, timedelta
from core.logger import log
from core.setting import config
from core.cache import get_global_kv
from core.proxy import global_request
import jwt
from model.User import User
from model.RoleScope import RoleScope
from model.UserRole import UserRole
from core.cache import MemStorage
from lib.hash import hash_util

user_scopes = {
    "user:read" : "Read user information",
    "user:write" : "Write user information",
    "user:create": "Create user",
    "user:delete": "Delete user",
    "system:read": "get system information",
    "system:write": "modify system information",
}

role_scopes = {
    "admin": ["user:read", "user:write", "user:create", "user:delete", "system:read", "system:write"],
    "user": ["user:read", "user:write"]
}

oauth2_depends = OAuth2PasswordBearer("/authorization/token", scopes=user_scopes)


def create_access_token(data: Dict) -> str:
    """
    construct JWT token
    param data is the payload of jwt token, header and signature are added automatically
    :param data: payload
    :return: token string
    """
    """
    additional_headers = {"alg": "HS256", "typ": "JWT"}
    in RFC7519  https://www.rfc-editor.org/rfc/rfc7519:
    "iss" (Issuer), APP_NAME
    "sub" (Subject), title / subject / user id (usually)
    "aud" (Audience),
    "exp" (Expiration Time),
    "nbf" (Not Before), 生效时间
    "iat" (Issued At), 
    "jti" (JWT ID) JWT ID
    Private Claim Names
    1. "uid" (User) 用户ID
    2. "scope" (Permissions)  looks like [<...>, <...>]
    """
    token_data = data.copy()
    expire = datetime.now() + timedelta(minutes=config.JWT_ACCESS_EXPIRE_MINUTES)  # JWT过期分钟 = 当前时间 + 过期时间
    iat = datetime.now()
    jti = uuid.uuid4().hex
    token_data.update(
        {
            "exp": expire, 
            "iss": config.APP_NAME,
            "jti": jti,
            "iat": iat,
        }
    )
    jwt_token = jwt.encode(
        payload=token_data,             # payload
        key=config.JWT_SECRET_KEY,      # key for signature, usually a secret
        algorithm=config.JWT_ALGORITHM  # default is HS256
    )
    log.debug(f"a jwt token is created with {token_data} at {iat}, expire at {expire}")
    return jwt_token


def scope_contains(access_required_scope:list, user_has_scope:list) -> bool:
    """
    check if the required scope is included in the user's scope
    :param access_required_scope: resources requeired
    :param user_has_scope: user's scope
    :return: bool
    """
    return set(access_required_scope).issubset(set(user_has_scope))


async def check_permissions(
        req: Request,
        required_scope: SecurityScopes, 
        token=Depends(oauth2_depends),
        runtime_state:MemStorage = Depends(get_global_kv)) -> None:
    
    """
    check user's permission
    the function will be injected into the endpoint function as a dependency, 
     if no exception is raised, the user has the permission to access the resource.
    :param req: request object
    :param required_scope: what resources user needs to access
    :param token: token string
    :param runtime_state: global state
    """
    
    payload = None
    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
        log.debug(f"a payload has been decoded from token: {payload}")
        runtime_state.set_value(payload.get("sub"),True)
        if not payload:
            raise HTTPException(401, "Invalid certification", {"WWW-Authenticate": f"Bearer {token}"})
    except jwt.ExpiredSignatureError:
        raise HTTPException("Certification has expired", {"WWW-Authenticate": f"Bearer {token}"})
    except jwt.InvalidTokenError:
        raise HTTPException("Certification parse error", {"WWW-Authenticate": f"Bearer {token}"})
    except jwt.PyJWTError:
        raise HTTPException("Certification parse failed", {"WWW-Authenticate": f"Bearer {token}"})
    
    user_requested_scope = payload.get("scope")


    if scope_contains(required_scope.scopes, user_requested_scope) is False:
        raise HTTPException("Not enough scope for authorization", {"WWW-Authenticate": f"Bearer {token}"})
    
    global_request.userinfo = payload
    """
    userinfo fields:
    1. sub: user id
    2. scope: user permissions
    """



def verify_password(password:str, hashed_password:str) -> bool: # verify password
    return hash_util.verify_bcrypt(password, hashed_password)

async def verify_user_credentials(username: str, password: str) -> Union[None, User]:
    log.debug(f"verifying user credentials for {username}, with password {password}")
    user = await User.filter(username=username).first()
    if not user:
        return None
    if not user.is_active:
        return None
    log.debug(f"user {username} is active, verifying password => {user.password}")
    if not verify_password(password, user.password):
        return None
    return user

def hash_password(password) -> str:
    return hash_util.bcrypt(password)

async def get_user_permissions(username: str) -> list:
    user = await User.filter(username=username).first()
    if not user:
        return []
    user.user_id
    roles = await UserRole.filter(user_id=user.user_id).first()
    if not roles:
        return []
    
    permissions = []
    for role in roles.role.split(","):
        scope = await RoleScope.filter(role=role).first()
        if not scope:
            continue
        permissions.extend(scope.scopes.split(","))
    return permissions

