import logging
from logging.config import fileConfig

ARTICLE_PER_PAGE = 15
REPLY_PER_PAGE = 15
DEBUG = False
SITE_NAME = "PoolC"
DB_CONNECTION_STRING = 'sqlite:///sqlite.db'
REDIS_CONNECT_ARGS = {
    "host": "localhost",
    "port": 6379,
    "db": 0,
}
logger = logging.getLogger()
fileConfig("logger.cnf")