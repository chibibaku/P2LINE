#インポート=====================
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, events)
import json
import os

from linebot.models.messages import Message

#変数定義======================
app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

send = "None"
msg = "None"
replyUser = "SET REPLY USER"

##toLine
#callback====================

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    global msg
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global msg 
    msg = event.message.text
    #line_bot_api.reply_message(
    #    event.reply_token,
    #    TextSendMessage(text=event.message.text))



##toPyto
#curl_get====================

@app.route('/post',methods=["POST"])
def postget():
    global send
    send = request.get_data().decode('utf-8')
    try:
        line_bot_api.push_message(replyUser,TextSendMessage(text=send))
    except:
        return "error : msg = " + send
    return "ok"

#============================

@app.route('/pyto')
def pyto_check_respons():
    global msg
    return msg

#============================

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
