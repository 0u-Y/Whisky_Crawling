from bs4 import BeautifulSoup
import requests
from multiprocessing import Pool


whisky_number = list(range(1,1000))

base_url = "https://www.whiskybase.com/whiskies/whisky/{}"


whisky_info = []





headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}





def get_whisky_info(num):

    url = base_url.format(num)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')




        #위스키 정보
        whisky_title_tag = soup.find('h1').find('a')
        whisky_name = whisky_title_tag.get_text(strip=True)

        bottling_serie_label = soup.find('dt', string="Bottling serie")
        bottling_serie_value = bottling_serie_label.find_next_sibling('dd').get_text(strip=True) if bottling_serie_label else 'N/A'

        stated_age_label = soup.find('dt', string="Stated Age")
        stated_age_value = stated_age_label.find_next_sibling('dd').get_text(strip=True)  if stated_age_label else 'N/A'

        if stated_age_value != 'N/A':
            stated_age_value = stated_age_value.split('y')[0].rstrip()
        else:
            stated_age_value = 'N/A' 

        strength_label = soup.find('dt', string="Strength")
        strength_value = strength_label.find_next_sibling('dd').get_text(strip=True) if strength_label else 'N/A'

        if strength_value != 'N/A':
            strength_value = strength_value.split('V')[0].rstrip()
        else:
            strength_value = 'N/A'




        return ({
            '위스키 이름': whisky_name,
            'Bottling Serie': bottling_serie_value,
            'Stated Age': stated_age_value,
            '도수': strength_value,
        })
    
    return None


def collect_whisky_info():

    with Pool(processes=8) as pool:
        result = pool.map(get_whisky_info, whisky_number)

    return [r for r in result if r is not None]





