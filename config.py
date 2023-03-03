import os
from pydantic import BaseSettings,BaseModel
from kombu import Queue, Exchange
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))


class Settings(BaseSettings):
    SQLITE_SYNC_URL_PREFIX: str = os.getenv("SQLITE_SYNC_URL_PREFIX")
    SQLITE_ASYNC_URL_PREFIX: str = os.getenv("SQLITE_ASYNC_URL_PREFIX")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    JWT_APP_TOKEN_EXPIRE_TIME: int = 4
    JWT_REFRESH_TOKEN_EXPIRE_TIME: int = 5
    DEBUG: bool = False

    MAIL_SERVER: str = 'smtp.aol.com'
    MAIL_USERNAME: str = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD: str = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER: str = os.getenv('MAIL_DEFAULT_SENDER')
    MAIL_PORT: int = 587
    MAIL_USE_SSL: bool = False
    MAIL_USE_TLS: bool = True
    MAIL_MAX_EMAILS: int = 500

    class Config:
        env_file = ".env"

class TestSettings(BaseSettings):
    SQLITE_SYNC_URL_PREFIX_TEST: str = os.getenv("SQLITE_SYNC_URL_PREFIX_TEST")
    SQLITE_ASYNC_URL_PREFIX_TEST: str = os.getenv("SQLITE_ASYNC_URL_PREFIX_TEST")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    JWT_APP_TOKEN_EXPIRE_TIME: int = 4
    JWT_REFRESH_TOKEN_EXPIRE_TIME: int = 5
    DEBUG: bool = False

    MAIL_SERVER: str = 'smtp.aol.com'
    MAIL_USERNAME: str = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD: str = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER: str = os.getenv('MAIL_DEFAULT_SENDER')
    MAIL_PORT: int = 587
    MAIL_USE_SSL: bool = False
    MAIL_USE_TLS: bool = True
    MAIL_MAX_EMAILS: int = 500

    class Config:
        env_file = ".env"


class BaseCelery(BaseSettings):
    CELERY_broker_url: str = os.environ.get("CELERY_Broker_URL")
    RESULT_BACKEND: str = os.environ.get("RESULT_BACKEND")
    worker_concurrency = 2
    CELERY_TASK_QUEUES: list = (
        # default queue
        Queue("celery", Exchange('celery', type='direct'), routing_key='default'),
        Queue("opencelery", Exchange('opencelery', type='direct'), routing_key='opencelery'),
        Queue('useradmin', Exchange('useradmin', type='direct'), routing_key='useradmin')

    )
class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "erp_logger"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    }

settings = Settings()
celeryconf = BaseCelery().dict()
