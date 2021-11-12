# 必要モジュールの読み込み
import random
from flask import Flask, request, abort
import os
from future.utils import python_2_unicode_compatible
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import re

from aknanewords import words
from weather_data import get_weather

# 変数appにFlaskを代入。インスタンス化
app = Flask(__name__)

# 環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# Herokuログイン接続確認のためのメソッド
# Herokuにログインすると「hello world」とブラウザに表示される


@app.route("/")
def hello_world():
    return "hello world!"

# ユーザーからメッセージが送信された際、LINE Message APIからこちらのメソッドが呼び出される。


@app.route("/callback", methods=['POST'])
def callback():
    # リクエストヘッダーから署名検証のための値を取得
    signature = request.headers['X-Line-Signature']

    # リクエストボディを取得
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 署名を検証し、問題なければhandleに定義されている関数を呼び出す。
    try:
        handler.handle(body, signature)
    # 署名検証で失敗した場合、例外を出す。
    except InvalidSignatureError:
        abort(400)
    # handleの処理を終えればOK
    return 'OK'

# LINEでMessageEvent（普通のメッセージを送信された場合）が起こった場合に、
# def以下の関数を実行します。
# reply_messageの第一引数のevent.reply_tokenは、イベントの応答に用いるトークンです。
# 第二引数には、linebot.modelsに定義されている返信用のTextSendMessageオブジェクトを渡しています。


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "help":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='アカネチャンという文字を含めて話しかけてな'))
    elif event.message.text == "天気":
        result = get_weather()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=str(result)))
    elif re.search('アカネチャン', event.message.text):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=random.choice(words)))


# ポート番号の設定
if __name__ == "__main__":
    #    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
