import requests
from bs4 import BeautifulSoup
import json


def query_search(query):
    url = f'https://search.wb.ru/exactmatch/ru/male/v4/search?appType=1&couponsGeo=7,3,6,22,21&curr=rub&dest=-7216354&emp=0&lang=ru&locale=ru&pricemarginCoeff=1.0&query={query}&reg=1&regions=80,4,115,83,68,70,69,30,86,40,1,66,31,48,110,22,111&resultset=catalog&sort=popular&spp=25&sppFixGeo=4&suppressSpellcheck=false'
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    site_json = json.loads(soup.text)
    if not site_json['data']['products']:
        return None
    result = {}
    n = 0
    for i in site_json['data']['products']:
        result.update({i['name']: f"https://www.wildberries.ru/catalog/{i['id']}/detail.aspx?targetUrl=MI"})
        n += 1
        if n > 9:
            break

    return result
