import requests
from bs4 import BeautifulSoup

urls = ['https://tenki.jp/forecast/3/13/4210/10203/',
       'https://tenki.jp/forecast/3/13/4210/10201/',
       'https://tenki.jp/forecast/3/11/4020/8219/'
]
def get_weather():
    for url in urls:
        res = requests.get(url)
        html = BeautifulSoup(res.text, 'html.parser')
        title = html.find('h2').get_text().split('の')
        weather = html.find('p',{'class': 'weather-telop'}).get_text()
        weather = '\n'.join([title[0], weather])
        return weather


