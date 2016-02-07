from bs4 import BeautifulSoup
import requests
from json import dumps


URL = 'http://bluediamond.3dcartstores.com/'


def get_urls(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    categories = soup.find_all('a', {'class': 'secondary'})
    categories = categories[:-1]
    category_urls = [str(url) + str(link.get('href')) for link in categories]

    item_urls = []
    for c_url in category_urls:
        r = requests.get(c_url)
        soup = BeautifulSoup(r.content)
        items = soup.find_all('a')
        for i in items:
            if i.text == 'View Product Detail':
                item_urls.append(str(url) + str(i.get('href')))

    get_info(item_urls)


def get_info(url_list):
    info = {}
    for url in url_list:
        r = requests.get(url)
        soup = BeautifulSoup(r.content)

        name = soup.find('h2').text
        details = soup.find('p').text
        price = soup.find(id='price').text
        image = soup.find('img', {'id': 'large'}).get('src')

        info[name] = {'details': details,
                     'price': price.split(':')[-1],
                     'image': image
                     }

    with open('bd_info.json', 'w') as f:
        f.write(dumps(info))


get_urls(URL)
