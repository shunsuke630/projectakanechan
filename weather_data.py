from future.utils import ensure_new_type
import requests
from bs4 import BeautifulSoup

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
    
    for result in weathers:
        result = "\n".join(result)
    
    return result


