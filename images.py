import random
from linebot.models import ImageSendMessage

horror = ['https://i.gyazo.com/e54023898ac2a8d9902a4850a2a44bf0.jpg', 'https://i.gyazo.com/ba9501bd876e77c5d67332e6630a81c2.jpg', 'https://i.gyazo.com/606a3b329d0b247e1667fd998e2f3545.jpg']

def horror_image_message():
    url =random.choice(horror)
    messages = ImageSendMessage(
        original_content_url = url, #JPEG 最大画像サイズ：240×240 最大ファイルサイズ：1MB(注意:仕様が変わっていた)
        preview_image_url = url #JPEG 最大画像サイズ：1024×1024 最大ファイルサイズ：1MB(注意:仕様が変わっていた)
    )
    return messages
