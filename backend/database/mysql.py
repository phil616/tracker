from core.setting import config, get_db_models
from core.logger import log
def get_mysql_db_config() -> dict:
    log.info("Using SQLite as database")
    return {
        "connections": {
            "default": {  # base database named base
                'engine': 'tortoise.backends.mysql',
                "credentials": {
                    'host': config.DB_HOST,
                    'user': config.DB_USER,
                    'password': config.DB_PASS,  # password of mysql server
                    'port': config.DB_PORT,
                    'database': config.DB_NAME,  # name of mysql database server
                }
            },
        },
        "apps": {
            "models": {
                "models": get_db_models(),
                "default_connection": "default"
            },
        },
        'use_tz': True,
        'timezone': config.GLOBAL_TIMEZONE
    }