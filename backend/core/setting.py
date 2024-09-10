from pydantic_settings import BaseSettings
from pydantic import Field
from os import path, walk
from typing import List, Union
from core.logger import log

class Settings(BaseSettings):
    # ---- Project Basic Config ----
    APP_NAME: str = Field(default="Application API",env="APP_NAME",description="name of the application, also used as the jwt issuer")
    APP_DESC: str = Field(default="OpenAPI ",env="APP_DESCRIPTION",description="description of the application")
    APP_VER: str = Field(default="0.0.1",env="APP_VERSION",description="version of the application")

    ENABLE_USER_REGISTRATION: bool = Field(default=False,env="ENABLE_USER_REGISTRATION",description="是否允许用户通过邮箱注册，无域名状态不可用")
    SERVER_HOST: str = Field(default="localhost",env="SERVER_HOST",description="服务器IP地址")
    SERVER_PORT: int = Field(default=8000,env="SERVER_PORT",description="服务器端口")
    API_STR: str = Field(default="/api",env="API_STR",description="API前缀")
    DEBUG: bool = Field(default=True,env="DEBUG",description="是否开启调试模式")

    # ---- SMTP Settings ----
    SMTP_PORT: Union[int, str] = Field(default=587, env="SMTP_PORT", description="SMTP端口")
    SMTP_HOST: Union[str, None] = Field(default=None, env="SMTP_HOST", description="SMTP主机")
    SMTP_USER: Union[str, None] = Field(default=None, env="SMTP_USER", description="SMTP用户名")
    SMTP_PASSWORD: Union[str, None] = Field(default=None, env="SMTP_PASSWORD", description="SMTP密码")
    EMAILS_FROM_EMAIL: Union[str, None] = Field(default=None, env="EMAILS_FROM_EMAIL", description="发件人邮箱")

    # ---- CORS ---- # Cross-Origin Resource Sharing Policy
    CORS_ALLOW_ORIGINS: List = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List = ["*"]
    CORS_ALLOW_HEADERS: List = ["*"]

    # ---- Secure ---- # JWT (JSON Web Token)
    JWT_SECRET_KEY: str = Field(default="CHANGETHIS", env="JWT_SECRET_KEY", description="JWT密钥")
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM", description="JWT算法")
    JWT_ACCESS_EXPIRE_MINUTES: int = Field(default=60, env="JWT_ACCESS_EXPIRE_MINUTES",
                                           description="JWT访问过期时间（分钟）")
    # ---- Switches ----
    ENABLE_BACKEND_CORS_ORIGINS: bool = Field(default=True)  # enable this if on a remote public server
    ENABLE_STATIC_DIR: bool = Field(default=False)  # enable this if you want to serve static files
    MODEL_DIR: str = Field(default="model")

    # ---- SQLite FILE ----
    SQLITE_FILE: str = Field(default="db.sqlite3", env="SQLITE_FILE", description="SQLite文件名")

    # ---- Relational Database ----
    DB_HOST: str = Field(default="localhost", env="DB_HOST", description="数据库主机")
    DB_PORT: int = Field(default=3306, env="DB_PORT", description="数据库端口")
    DB_USER: str = Field(default="root", env="DB_USER", description="数据库用户名")
    DB_PASS: str = Field(default="root", env="DB_PASS", description="数据库密码")
    DB_NAME: str = Field(default="events", env="DB_NAME", description="数据库名")

    # ---- Redis Cache ----
    REDIS_HOST: str = Field(default="localhost", env="REDIS_HOST", description="Redis主机")
    REDIS_USER: Union[str, None] = Field(default=None, env="REDIS_USER", description="Redis用户名")
    REDIS_PORT: int = Field(default=6379, env="REDIS_PORT", description="Redis端口")
    REDIS_PASS: Union[str, None] = Field(default=None, env="REDIS_PASS", description="Redis密码")
    REDIS_DB: int = Field(default=0, env="REDIS_DB", description="Redis数据库")

    # ---- System Login ----
    SUPERUSER: str = Field(default="admin", env="SUPERUSER", description="登录用户名")
    SUPERPASS: str = Field(default="admin123", env="SUPERPASS", description="登录密码")
    SUPEREMAIL: str = Field(default="admin@localhost", env="SUPEREMAIL", description="登录邮箱")
    GLOBAL_TIMEZONE: str = Field(default="Asia/Shanghai", env="GLOBAL_TIMEZONE", description="时区")
    class Config:
        env_file = ".env"  # Path to a file containing environment variables

    ...


config = Settings()

def get_db_models():
    skip_files = ['AbstractBase.py', 'Basic.py', '__init__.py']  # skip package file and BaseTimestampMixin (Basic.py)
    ret = []
    for _, _, i in walk(path.join(config.MODEL_DIR)):
        models = list(set(i) - set(skip_files))
        for model in models:
            model = model.replace(".py", "")
            model = config.MODEL_DIR + "." + model
            ret.append(model)
        break
    log.info(f"models discover: {ret}")
    return ret
