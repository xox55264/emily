from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction, PostbackTemplateAction, PostbackEvent

def menu_template(text):
    menu_template = TemplateSendMessage(
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
    return menu_template
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