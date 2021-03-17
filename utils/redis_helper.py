import redis
import os

class RedisHelper(object):
    """docstring for RedisHelper"""
    def __init__(self):
        super(RedisHelper, self).__init__()
        self.r = redis.Redis(host=os.environ['REDIS_HOST'],
                             port=6379,
                             decode_responses=True)

    def get_value(self, key):
        return self.r.get(key)

    def set_value(self, key, value, expire=60):
        return self.r.set(key, value, ex=expire, nx=True)

    def compare_vaule(self, key, value):
        return value == self.get_value(key)

    def delete_key(self, key):
        return self.r.delete(key)

    def check_key_exist(self, key):
        return self.r.exists(key)