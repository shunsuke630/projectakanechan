import random
from linebot.models import ImageSendMessage

sweets = ['https://i.gyazo.com/606a3b329d0b247e1667fd998e2f3545.jpg',
          'https://gyazo.com/e63df89aaa30d3c215f60f5f0754d656.jpg',
          'https://gyazo.com/6b6d1e07cf5bcbff0d090415fff3dd34.jpg',
          'https://gyazo.com/b883830505ea68637488cfda387f9314'
        ]

def horror_image_message():
    url =random.choice(sweets)
    messages = ImageSendMessage(
        original_content_url = url, #JPEG 最大画像サイズ：240×240 最大ファイルサイズ：1MB(注意:仕様が変わっていた)
        preview_image_url = url #JPEG 最大画像サイズ：1024×1024 最大ファイルサイズ：1MB(注意:仕様が変わっていた)
    )
    return messages
