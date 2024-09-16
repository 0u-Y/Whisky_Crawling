from bs4 import BeautifulSoup
import requests
from multiprocessing import Pool
import time
import random


whisky_number = list(range(1,2000))

base_url = "https://www.whiskybase.com/whiskies/whisky/{}"


whisky_info = []



user_agents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
]




def get_whisky_info(num):

    headers = {
        "User-Agent": random.choice(user_agents)
    }

    time.sleep(random.uniform(1, 5))

    url = base_url.format(num)
    response = requests.get(url, headers=headers)


    time.sleep(random.uniform(1, 5))

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')


        whisky_name = None
        bottling_serie_value = 'N/A'
        stated_age_value = 'N/A'
        strength_value = 'N/A'
        overall_rating_value = 'N/A'



        #위스키 정보
        whisky_title_tag = soup.find('h1').find('a')
        if whisky_title_tag:
            whisky_name = whisky_title_tag.get_text(strip=True)


        bottling_serie_label = soup.find('dt', string="Bottling serie")
        if bottling_serie_label:
            bottling_serie_value = bottling_serie_label.find_next_sibling('dd').get_text(strip=True) if bottling_serie_label else 'N/A'

        stated_age_label = soup.find('dt', string="Stated Age")
        if stated_age_label:
            stated_age_value = stated_age_label.find_next_sibling('dd').get_text(strip=True)  if stated_age_label else 'N/A'
            if 'y' in stated_age_value:
                stated_age_value = stated_age_value.split('y')[0].rstrip()

        strength_label = soup.find('dt', string="Strength")
        if strength_label:
            strength_value = strength_label.find_next_sibling('dd').get_text(strip=True) if strength_label else 'N/A'
            if 'V' in strength_value:
                strength_value = strength_value.split('V')[0].rstrip()

        overall_rating_label = soup.find('dd', class_='votes-rating')
        if overall_rating_label:
            overall_rating_value = overall_rating_label.get_text(strip=True) if overall_rating_label else 'N/A'




        if whisky_name:
            return {
                'whisky_name': whisky_name,
                'bottling_serie': bottling_serie_value,
                'stated_age': stated_age_value,
                'strength': strength_value,
                'overall': overall_rating_value
            }
    
    return None


def collect_whisky_info():

    with Pool(processes=8) as pool:
        result = pool.map(get_whisky_info, whisky_number)

    return [r for r in result if r is not None]





