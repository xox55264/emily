import redis
import os
import configparser

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

class StatusHelper(object):
    def __init__(self):
        super(StatusHelper, self).__init__()
        self.redis_helper = RedisHelper()
        self.config = configparser.ConfigParser(allow_no_value=True)
        self.config.read('status.conf')

    def get_status(self, user_id):
        return self.redis_helper.get_value(f'{user_id}_status')

    def set_status(self, status, user_id):
        return self.redis_helper.set_value(f'{user_id}_status', status)

    def check_status(self, status, user_id):
        return self.redis_helper.get_value(f'{user_id}_status') == self.config[status]['prev_status']

    def get_next_status(self, status):
        return self.config[status]['next_status']