import logging
from dataclasses import dataclass
from os import getenv

from arq.connections import RedisSettings


@dataclass
class RedisConfig:
    """Redis connection variables"""

    db: str = int(getenv("REDIS_DATABASE", 1))
    host: str = getenv("REDIS_HOST", "containers-us-west-40.railway.app")
    port: int = int(getenv("REDIS_PORT", 6460))
    passwd: int = getenv("REDIS_PASSWORD", '4ZxLzxTFackwwN7goksA')
    username: int = getenv("REDIS_USERNAME", 'default')
    state_ttl: int = getenv("REDIS_TTL_STATE", None)
    data_ttl: int = getenv("REDIS_TTL_DATA", None)
    pool_settings = RedisSettings(host=host, port=port,password=passwd, database=db, username=username)




@dataclass
class Configuration:
    """All in one configuration's class"""

    debug = bool(getenv("DEBUG"))
    logging_level = int(getenv("LOGGING_LEVEL", logging.INFO))


    redis = RedisConfig()



conf = Configuration()