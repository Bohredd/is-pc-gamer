import requests
from bs4 import BeautifulSoup
from utils import has_next_page

url = "https://versus.com/br/graphics-card"

infos_obtidas = []

page = 1

while True:
    next_param = f"?page={page}&sort=versusScore"

    response = requests.get(f"{url}{next_param}")

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        list_div = soup.find('div', class_='List__list___3KkED')

        if list_div:
            items = list_div.find_all('div', class_=lambda x: x and x.startswith('Item__item_'))

            for item in items:
                item_info = {}

                top_container = item.find('div', class_=lambda x: x and x.startswith('Item__topContainer_'))
                if top_container:
                    item_info['top_container'] = top_container.get_text(strip=True)

                    name_and_props = top_container.find('div', class_=lambda x: x and x.startswith('Item__nameAndProps_'))
                    if name_and_props:
                        item_info['name_and_props'] = name_and_props.get_text(strip=True)

                score_container = item.find('div', class_=lambda x: x and x.startswith('Item__scoreContainer_'))
                if score_container:
                    item_info['score_container'] = score_container.get_text(strip=True)

                infos_obtidas.append(item_info)

            if has_next_page(soup):
                page += 1
            else:
                break
        else:
            break
    else:
        break

for info in infos_obtidas:
    print(info)

print("Paginas percorridas: ", page)