from aioredis import Redis
from core.setting import config

async def get_redis_connection():
    redis = await Redis.from_url(f'redis://{config.REDIS_USER}:{config.REDIS_PASS}@{config.REDIS_HOST}:{config.REDIS_PORT}/{config.REDIS_DB}')
    # redis://[[username]:[password]]@localhost:6379/0
    try:
        yield redis
    finally:
        await redis.close()

