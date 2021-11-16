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
    DatetimePickerAction, messages,DatetimePickerTemplateAction
)
import re
from linebot.models.events import PostbackEvent

from linebot.models.template import ButtonsTemplate

from aknanewords import words
from weather_data import get_weather
from linebot.models import ImageSendMessage
from images import horror_image_message

import firebase_admin
from firebase_admin import credentials
from google.cloud import storage

# 変数appにFlaskを代入。インスタンス化
app = Flask(__name__)

# 環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
# Firebaseの認証情報
# GOOGLE_APPLICATION_CREDENTIALS=os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
# # Firebaseのバケット先
# FIREBASE_STORAGE_BUCKET=os.environ["FIREBASE_STORAGE_BUCKET"]
# cred = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS)
# firebase_admin.initialize_app(cred, {
#     'storageBucket': FIREBASE_STORAGE_BUCKET
# })

# # インスタンス作成
# client = storage.Client()
# bucket = client.get_bucket(FIREBASE_STORAGE_BUCKET)


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
    message = event.message.text #メッセージ内容
    # group_id = event.source.group_id() #グループID
    # user_id = event.source.user_id() #ユーザID
    # profile = line_bot_api.get_group_member_profile(group_id, user_id)
    # if event.message.text == "help":
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         TextSendMessage(text='アカネチャンという文字を含めて話しかけてな'))
    # elif event.message.text == "天気":
    #     result = get_weather()
    #     result = "\n".join(result)
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         TextSendMessage(text=result))
    # elif re.search('アカネチャン', event.message.text):
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         TextSendMessage(text=random.choice(words)))
    # elif event.message.text == "シフォンケーキ":
    #     image_data = horror_image_message()
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         image_data)
    if message == "登録":
        date_picker = TemplateSendMessage(
                alt_text='誕生日を設定',
                template=ButtonsTemplate(
                    text='さんの誕生日を設定します',
                    title='誕生日通知システム',
                    actions=[ 
                    DatetimePickerAction(
                            label='誕生日を登録する',
                            date='action=regist&&mode=date',
                            mode="date",
                            initial='1998-01-01',
                            min='1980-01-01',
                            max='2100-01-01'
                    )
                    ]
                )
        )
        line_bot_api.reply_message(
            event.reply_token,
            date_picker
        )
    
# @handler.add(PostbackEvent)
# def handle_postback(event):
#     group_id = event.source.group_id # グループID
#     user_id = event.source.user_id # ユーザーID
#     profile = line_bot_api.get_group_member_profile(group_id, user_id) # ユーザーのプロファイル
#     dateString = event.postback.params['date'] # datePickerから送信された日付
#     birthday_triming = dateString.split('-')
#     if event.postback.data == 'action=regist&&mode=date':
#         registe_birthday(
#             group_id,
#             profile.display_name,
#             user_id,
#             dateString
#         )
#         month = int(birthday_triming[1])
#         day = int(birthday_triming[2])
#         line_bot_api.reply_message(
#             event.reply_token, TextSendMessage(text=f'{profile.display_name}さんが誕生日を登録しました！\n{month}月{day}日に通知します✨'))

# def registe_birthday(group_id,display_name,user_id,birthday):
#     file_path = f'birthday/{group_id}.csv' # グループIDをファイル名にする
#     blob = bucket.blob(file_path) # ストレージのパスを指定
#     # - で分割して年月日を配列に格納
#     # (例: birthday_triming[0] = 2021, birthday_triming[1] = 8, birthday_triming[2] = 28)
#     birthday_triming = birthday.split('-')
#     month = birthday_triming[1]
#     day = birthday_triming[2]
#     # LINEでの表示名,ユーザー識別ID,月,日を文字列として連結
#     write_texts = [f"{display_name},{user_id},{month},{day}"]
#     if blob.exists():
#         input_file = blob.open()
#         datalist = input_file.read().splitlines()
#         for line in datalist:
#             if f"{user_id}" in line:
#                 continue
#             else:
#                 write_texts.append(line)
#     csv_string_to_upload = "" 
#     for text in write_texts:
#         csv_string_to_upload += text + "\n"
#     # Firebase Storageにアップロードする
#     blob.upload_from_string(
#         data=csv_string_to_upload,
#         content_type='text/csv'
#         )

# ポート番号の設定
if __name__ == "__main__":
    #    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
