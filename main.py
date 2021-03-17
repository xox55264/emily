import os
import json
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction, PostbackTemplateAction, PostbackEvent
from utils.intention import Accounting, Intention
from utils.helper import StatusHelper

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
    user_id = event.source.user_id
    status = status_helper.get_status(user_id)
    print(status)
    if status == 'accounting_date':
        data = {'status': status, 'date': event.message.text}
        reply_template = accounting_template.get_date(data, user_id)
    elif status == 'accounting_item':
        data = {'status': status, 'item': event.message.text}
        reply_template = accounting_template.get_item(data, user_id)
    elif status == 'accounting_amount':
        data = {'status': status, 'item': event.message.text}
        reply_template = accounting_template.get_amount(data, user_id)
    elif status == 'accounting_price':
        data = {'status': status, 'item': event.message.text}
        reply_template = accounting_template.get_price(data, user_id)

    else:
        reply_template = Intention.menu(False)

    line_bot_api.reply_message(
        event.reply_token,
        reply_template
        )

@handler.add(PostbackEvent)
def handle_postback(event):
    data = json.loads(event.postback.data, strict=False)
    user_id = event.source.user_id
    if status_helper.check_status(data['status'], user_id):
        if data['status'] == 'accounting':
            reply_template = accounting_template.start_accounting(data, user_id)

        elif data['status'] == 'accounting_date':
            reply_template = accounting_template.get_date(data, user_id)

        line_bot_api.reply_message(
            event.reply_token,
            reply_template)
    else:
        line_bot_api.reply_message(
            event.reply_token,
            Intention.menu(False))

if __name__ == "__main__":
    status_helper = StatusHelper()
    accounting_template = Accounting()
    app.run(debug=True, host='0.0.0.0', port=6969)