# import linebot
import requests
from bs4 import BeautifulSoup
# import os
# from datetime import datetime,timedelta,timezone
# from linebot import LineBotApi
# from linebot.models import TextSendMessage

# YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
# line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)

urls = ['https://tenki.jp/forecast/3/13/4210/10203/',
       'https://tenki.jp/forecast/3/13/4210/10201/',
       'https://tenki.jp/forecast/3/11/4020/8219/'
]
def get_weather():
    weathers = []
    for url in urls:
        res = requests.get(url)
        html = BeautifulSoup(res.text, 'html.parser')
        title = html.find('h2').get_text().split('の')
        weather = html.find('p',{'class': 'weather-telop'}).get_text()
        weather = [title[0],weather]
        weathers.append(weather)

    weather_data = []
    for result in weathers:
        weather_data.extend(result)

    return weather_data

# def check_weather():
#     dt_now = datetime.now()

    
