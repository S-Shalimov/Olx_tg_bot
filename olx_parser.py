import aiohttp
import asyncio
import bs4
from urls import *
from datetime import datetime, time
import re
from misc import *


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def get_soup(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    return soup

async def parse(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        soup = await get_soup(html)
        return soup

async def get_advertisements(url, amount=None):
    advertisements_lst = []
    soup = await parse(url)
    advertisements_html = soup.find_all('div', class_='css-1sw7q4x', attrs={'data-cy': 'l-card'})
    i = 0
    for advirsement in advertisements_html:
        advertisements_lst.append(dict())
        href = advirsement.find('a', class_='css-rc5s2u')['href']
        try:
            text_date_publ = advirsement.find('p', class_='css-1dfbw0k').get_text()
        except AttributeError:
            text_date_publ = advirsement.find('p', class_='css-veheph er34gjf0').get_text()
        if 'Сегодня в' in text_date_publ:
            date_publ = datetime.now().date()
            text_date_publ = re.search(r'\b\d{2}:\d{2}\b', text_date_publ).group()
            datetime_publ = datetime.combine(date_publ, datetime.strptime(text_date_publ, '%H:%M').time())
        else:
            for month, eng in RU_MON_TO_EN.items():
                if month in text_date_publ:
                    num_text_date_publ = re.sub(month, eng, text_date_publ)
            num_text_date_publ = re.search(r"\b\d{2} \w+ 2023\b", num_text_date_publ)
            date_obj = datetime.strptime(num_text_date_publ.group(), "%d %B %Y").date()
            time_obj = datetime.strptime("00:00", "%H:%M").time()
            datetime_publ = datetime.combine(date_obj, time_obj)
        advertisements_lst[i]['datetime_publ'] = datetime_publ
        advertisements_lst[i]['href'] = href
        i += 1
        if amount is not None:
            amount -= 1
        if amount is not None and amount <= 0:
            break
    return advertisements_lst, amount

async def count_pages(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        soup = await get_soup(html)
    pages_nums = soup.find_all('a', class_='css-1mi714g')
    list_pages_nums = [int(page.text) for page in pages_nums]
    max_num_page = max(list_pages_nums)
    return max_num_page

def sort_advertisements_lst(advertisements_lst):
    return sorted(advertisements_lst, key=lambda x: x['datetime_publ'], reverse=True)

async def main_get_advertisements(url, amount=None, sort_new=False):
    advertisements_lst, amount = await get_advertisements(url, amount=amount)
    max_num_page = await count_pages(url)
    for page in range(1, max_num_page + 1):
        if amount > 0:
            print('new iter')
            advertisements_lst_page, amount = await get_advertisements(url=(url + f'&page={page}'), amount=amount)
            for elem in advertisements_lst_page:
                advertisements_lst.append(elem)
    if sort_new == True:
        advertisements_lst = sort_advertisements_lst(advertisements_lst)
    for elem in advertisements_lst:
        elem_url = URL_MAIN + elem['href']
        soup = await parse(elem_url)
        title = soup.find('h1', class_='css-1soizd2 er34gjf0')
        desc = soup.find('div', class_='css-b7rzo5 er34gjf0')
        price = soup.find('h3', class_='css-ddweki er34gjf0')
        if price is None:
            price = soup.find('p', class_='css-b5m1rv er34gjf0')
        features_lst = soup.find('ul', class_='css-sfcl1s')
        if features_lst is not None:
            features = features_lst.find_all('li', class_='css-b5m1rv er34gjf0')
        else:
            features = None
        name = soup.find('h4', class_='css-1lcz6o7 er34gjf0')
        place = soup.find('p', class_='css-1cju8pu er34gjf0')
        img_main = soup.find('img', class_='css-1bmvjcs')
        img_other = soup.find_all('img', class_='swiper-lazy css-1bmvjcs swiper-lazy-loaded')
        img_other = None if not img_other else img_other

        imgs = None
        if img_main is not None:
            imgs = list()
            imgs.append(img_main.get('src'))
        if img_other is not None:
            if imgs is None:
                imgs = list()
            for img_other_elem in img_other:
                imgs.append(img_other_elem.get('src'))

        #elem['phone'] = phone.text
        elem['title'] = title.text
        if desc is not None:
            elem['desc'] = desc.text
        else:
            elem['desc'] = 'None'
        if price is not None:
            elem['price'] = price.text
        else:
            elem['price'] = 'None'
        if features is not None:
            elem['features'] = [feature.text for feature in features]
        else:
            elem['features'] = 'None'
        if name is not None:
            elem['name'] = name.text
        else:
            elem['name'] = 'None'
        if place is not None:
            elem['place'] = place.text
        else:
            elem['place'] = 'None'
        if imgs is not None:
            elem['img'] = imgs
        else:
            elem['img'] = 'None'
    return advertisements_lst
#todo: add phone

