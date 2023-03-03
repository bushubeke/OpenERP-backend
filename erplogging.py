import logging
from logging.config import dictConfig
from config import LogConfig


dictConfig(LogConfig().dict())
logger = logging.getLogger("erp_logger")

filehandler=logging.FileHandler('record.log')
filehandler.setLevel(logging.INFO)
logger.addHandler(filehandler)

logger.setLevel(logging.INFO)
