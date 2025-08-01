import redis
from var import var

INFO = var.REDIS['URL'].split(':')

DB = redis.StrictRedis(
    host=INFO[0],
    port=INFO[1],
    password=var.REDIS['PASS'],
    decode_responses=True,
)