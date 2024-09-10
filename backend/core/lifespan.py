from fastapi import FastAPI
import contextlib
from core.logger import log
from core.sequence import setup, teardown

@contextlib.asynccontextmanager
async def app_lifespan(app: FastAPI):

    log.info("Starting Up lifespan")
    await setup()
    yield
    log.info("Shutting Down lifespan")
    await teardown()