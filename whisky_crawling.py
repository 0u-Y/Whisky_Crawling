from bs4 import BeautifulSoup
import requests
import pandas as pd




whisky_number = list(range(1,50))

base_url = "https://www.whiskybase.com/whiskies/whisky/{}"


whisky_info = []




headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}




    

for num in whisky_number:
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

        strength_label = soup.find('dt', string="Strength")
        strength_value = strength_label.find_next_sibling('dd').get_text(strip=True) if strength_label else 'N/A'


        whisky_info.append({
            '위스키 이름': whisky_name,
            'Bottling Serie': bottling_serie_value,
            'Stated Age': stated_age_value,
            '도수': strength_value
        })




def print_whisky_info():
    df = pd.DataFrame(whisky_info)

    print(df)


print_whisky_info()

















    

        

        



    



