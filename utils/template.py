from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction, PostbackTemplateAction, PostbackEvent
from datetime import datetime, timedelta
import json

def menu_template(text):
    template = TemplateSendMessage(
            alt_text=text,
            template=ButtonsTemplate(
                text=text,
                actions=[
                    PostbackTemplateAction(
                        label='記帳',
                        data='{"status":"accounting"}'
                    )
                ]
            )
    )
    return template

def date_template(status, text):
    today = datetime.today().date()
    yesterday = datetime.today().date()-timedelta(days=1)
    today_data = {'status': status, 'date': str(today)}
    yesterday_data = {'status': status, 'date': str(yesterday)}
    other_data = {'status': status, 'date': None}
    template = TemplateSendMessage(
            alt_text=text,
            template=ButtonsTemplate(
                text=text,
                actions=[
                    PostbackTemplateAction(
                        label='今天',
                        data=json.dumps(today_data)
                    ),
                    PostbackTemplateAction(
                        label='昨天',
                        data=json.dumps(yesterday_data)
                    ),
                    PostbackTemplateAction(
                        label='自行輸入',
                        data=json.dumps(other_data)
                    )
                ]
            )
    )
    return template

'''
TemplateSendMessage(
        alt_text='test alt text',
        template=ButtonsTemplate(
            title='這是ButtonsTemplate',
            text='ButtonsTemplate可以傳送text,uri',
            actions=[
                PostbackTemplateAction(
                    label='test label1',
                    data='a=1&b=2'
                ),
                PostbackTemplateAction(
                    label='test label2',
                    data='{"a":"123", "b": "456"}'
                )
            ]
        )
'''