import config
import redis
import os


if config.ENV == 'production':
    r = redis.from_url(os.environ.get("REDIS_URL"), decode_responses=True)
elif config.ENV == 'development':
    r = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)