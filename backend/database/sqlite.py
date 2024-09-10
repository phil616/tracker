
from os import path
from core.setting import config, get_db_models
from core.logger import log
def get_sqlite_db_config() -> dict:
    log.info("Using SQLite as database")
    return {
    "connections": {
        "default": {
            "engine": "tortoise.backends.sqlite",
            "credentials": {"file_path": path.join("storage", config.SQLITE_FILE)},
            }
        },
        "apps": {
            "events": {"models": get_db_models(), "default_connection": "default"}
        },
        "timezone": "Asia/Shanghai",
        "use_tz": config.GLOBAL_TIMEZONE,
    }
