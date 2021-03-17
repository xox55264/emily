import os
import json
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction, PostbackTemplateAction, PostbackEvent
from intentions import accounting


app = Flask(__name__)
line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])

@app.route('/chatbot')
def hello_world():
    return 'Hello, World!'

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    reply_text = TextSendMessage(text=event.message.text)
    template_message = TemplateSendMessage(
        alt_text='test alt text',
        template=ButtonsTemplate(
            title='這是ButtonsTemplate',
            text='ButtonsTemplate可以傳送text,uri',
            actions=[
                MessageTemplateAction(
                    label='ButtonsTemplate',
                    text='ButtonsTemplate'
                ),
                PostbackTemplateAction(
                    label='test label',
                    data='{"a":"123", "b": "456"}'
                )
            ]
        )
    )
    line_bot_api.reply_message(
        event.reply_token,
        [template_message, reply_text])

@handler.add(PostbackEvent)
def handle_postback(event):
    reply_text = TextSendMessage(text='postback event')
    data = json.loads(event.postback.data, strict=False)
    # if data['status'] == 'accounting':
    #     reply_message =
    template_message = TemplateSendMessage(
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
    )
    print(event.source.user_id)
    line_bot_api.reply_message(
        event.reply_token,
        [template_message, reply_text])

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=6969)