from utils import template
from utils.helper import StatusHelper


class Intention(object):
    def __init__(self):
        super(Intention, self).__init__()
        self.status_helper = StatusHelper()

    @staticmethod
    def menu(status_checking):
        text = '有什麼需要幫忙的嗎？' if status_checking else '你剛說啥來著？我忘了...'
        return template.menu_template(text)

class Accounting(Intention):
    def __init__(self):
        super(Accounting, self).__init__()

    def start_accounting(self, data, user_id):
        reply_template = template.date_template(self.status_helper.get_next_status(data['status']), '請輸入記帳日期')
        return reply_template

    # def get_date(self, data):
    #     template = template.date_template(self.status_helper.get_next_status(data['status']), '請輸入記帳日期')
    #     pass