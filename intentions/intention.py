import configparser

from utils import redis_helper, template


class Intention(object):
    def __init__(self):
        super(Intention, self).__init__()
        self.config = configparser.ConfigParser(allow_no_value=True)
        self.config.read('status.conf')
        self.redis_helper = redis_helper.RedisHelper()

    def check_status(self, status, user_id):
        return self.redis_helper.get_value(f'{user_id}_status') == self.config[status]['prev_status']

    def menu(self, status_checking):
        text = '有什麼需要幫忙的嗎？' if status_checking else '你剛說啥來著？我忘了...'
        return template.menu_template(text)
