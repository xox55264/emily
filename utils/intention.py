from utils import template
from utils.helper import StatusHelper, RedisHelper


class Intention(object):
    def __init__(self):
        super(Intention, self).__init__()
        self.status_helper = StatusHelper()
        self.redis_helper = RedisHelper

    @staticmethod
    def menu(status_checking):
        text = '有什麼需要幫忙的嗎？' if status_checking else '你剛說啥來著？我忘了...'
        return template.menu_template(text)

    def simple_text_processer(self, status, user_id, text):
        status_update = self.status_helper.set_status(self.status_helper.get_next_status(status), user_id)
        if status_update:
            reply_template = template.item_template(text)
            return reply_template, status_update

    def set_temporary_data(self, status, user_id, value):
        return self.redis_helper.set_value(f'{status}_{user_id}', value)

    def get_temporary_data(self, status, user_id, value):
        return self.redis_helper.get_value(f'{status}_{user_id}')

    def simple_message_processer(self, status, user_id, value, text):
        reply_template, status_update = self.simple_text_processer(status, user_id, text)
        data_storage = self.set_temporary_data(status, user_id, value)
        if data_storage & status_update:
            return reply_template





class Accounting(Intention):
    def __init__(self):
        super(Accounting, self).__init__()

    def start_accounting(self, data):
        reply_template = template.date_template(self.status_helper.get_next_status(data['status']), '請輸入記帳日期')
        return reply_template

    def get_date(self, data, user_id):
        # print(data['date'])
        # if data['date']:
        #     reply_template = self.simple_message_processer(data['status'], user_id, data['date'], '請輸入項目')
        # else:
        #     reply_template = template.simple_text_template('請輸入記帳日期，格式為YYYY-mm-dd')
        # return reply_template
        reply_template = self.simple_message_processer(data['status'], user_id, data['date'], '項目')
        return reply_template

    def get_item(self, data, user_id):
        reply_template = self.simple_message_processer(data['status'], user_id, data['item'], '請輸入數量（數字）')
        return reply_template

    def get_amount(self, data, user_id):
        reply_template = self.simple_message_processer(data['status'], user_id, data['amount'], '請輸入金額（數字）')
        return reply_template

    def get_price(self, data, user_id):
        date = self.get_temporary_data('accounting_date', user_id)
        item = self.get_temporary_data('accounting_item', user_id)
        amount = self.get_temporary_data('accounting_amount', user_id)
        price = data['price']
        reply_template = self.simple_text_processer(data['status'], user_id, '請輸入項目（數字）')
        return reply_template
