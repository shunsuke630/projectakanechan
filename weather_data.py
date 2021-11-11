import requests
from bs4 import BeautifulSoup

url = 'https://tenki.jp/forecast/3/13/4210/10203/'


def get_weather():
    res = requests.get(url)
    html = BeautifulSoup(res.text, 'html.parser')
    title = html.find('h2').get_text().split('の')
    weather = html.find('p',{'class': 'weather-telop'}).get_text()
    weather = [title[0], weather]
    return weather


