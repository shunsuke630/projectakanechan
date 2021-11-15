# 必要モジュールの読み込み
from datetime import date, datetime, timedelta
import random
from flask import Flask, request, abort
import os
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage,
    DatetimePickerAction,
)
import re
from linebot.models.events import PostbackEvent

from linebot.models.template import ButtonsTemplate

from aknanewords import words
from weather_data import get_weather
from linebot.models import ImageSendMessage
from images import horror_image_message

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
    group_id = event.source.group_id #グループID
    user_id = event.source.user_id #ユーザID
    profile = line_bot_api.get_group_member_profile(group_id, user_id)
    if event.message.text == "help":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='アカネチャンという文字を含めて話しかけてな'))
    elif event.message.text == "天気":
        result = get_weather()
        result = "\n".join(result)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=result))
    elif re.search('アカネチャン', event.message.text):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=random.choice(words)))
    elif event.message.text == "プリン":
        image_data = make_image_message()
        line_bot_api.reply_message(
            event.reply_token,
            image_data)
    elif event.message.text == "シフォンケーキ":
        image_data = horror_image_message()
        line_bot_api.reply_message(
            event.reply_token,
            image_data)
    elif "何でも言うことを聞いてくれるアカネチャン" in event.message.text and '登録' in event.message.text:
        date_picker = TemplateSendMessage(
                    alt_text = '誕生日を設定',
                    template = ButtonsTemplate(
                        text = f'{profile.display_name}さんの誕生日を設定します',
                        title = '誕生日通知システム',
                        actions =[ 
                        DatetimePickerAction(
                                label = '誕生日を登録する',
                                date = 'action=regist&&mode=date',
                                mode = "date",
                                initial = '1998-01-01',
                                min = '1980-01-01',
                                max = '2100-01-01'
                        )
                        ]
                    )
        )
        line_bot_api.reply_message(
            event.reply_token,
            date_picker
        )
    

def make_image_message():
    
    messages = ImageSendMessage(
        original_content_url = 'https://i.gyazo.com/0aff0fbedd9286058065c158187cedb2.jpg', #JPEG 最大画像サイズ：240×240 最大ファイルサイズ：1MB(注意:仕様が変わっていた)
        preview_image_url = 'https://i.gyazo.com/0aff0fbedd9286058065c158187cedb2.jpg' #JPEG 最大画像サイズ：1024×1024 最大ファイルサイズ：1MB(注意:仕様が変わっていた)
    )
    return messages

# @handler.add(PostbackEvent)
# def handle_postback(event):



# ポート番号の設定
if __name__ == "__main__":
    #    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
