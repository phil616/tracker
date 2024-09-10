from fastapi import FastAPI, HTTPException
from tortoise.exceptions import BaseORMException

from core.lifespan import app_lifespan
from core.setting import config
from endpoint import v1
from response.exceptions import database_exception_handler, global_exception_handler

app = FastAPI(
    debug=config.DEBUG,
    title=config.APP_NAME,
    description=config.APP_DESC,
    version=config.APP_VER,
    lifespan=app_lifespan,
)

if config.ENABLE_BACKEND_CORS_ORIGINS:
    from fastapi.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.CORS_ALLOW_ORIGINS,
        allow_credentials=config.CORS_ALLOW_CREDENTIALS,
        allow_methods=config.CORS_ALLOW_METHODS,
        allow_headers=config.CORS_ALLOW_HEADERS,
    )

if config.ENABLE_STATIC_DIR:
    from fastapi.staticfiles import StaticFiles

    app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(v1.v1_router)


app.add_exception_handler(HTTPException, global_exception_handler)
app.add_exception_handler(BaseORMException, database_exception_handler)
