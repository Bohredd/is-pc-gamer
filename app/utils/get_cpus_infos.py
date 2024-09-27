import requests
from bs4 import BeautifulSoup

# from app.hardwares.models import CPU
from app.utils.has_next_page import has_next_page

url = "https://versus.com/br/cpu"

infos_obtidas = []

page = 1

while True:
    next_param = f"?page={page}&sort=versusScore"

    response = requests.get(f"{url}{next_param}")

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        list_div = soup.find("div", class_="List__list___3KkED")

        if list_div:
            items = list_div.find_all(
                "div", class_=lambda x: x and x.startswith("Item__item_")
            )

            for item in items:
                item_info = {}

                top_container = item.find(
                    "div", class_=lambda x: x and x.startswith("Item__topContainer_")
                )
                if top_container:
                    item_info["top_container"] = top_container.get_text(strip=True)

                    name_and_props = top_container.find(
                        "div",
                        class_=lambda x: x and x.startswith("Item__nameAndProps_"),
                    )
                    if name_and_props:
                        item_info["name_and_props"] = name_and_props.get_text(
                            strip=True
                        )

                score_container = item.find(
                    "div", class_=lambda x: x and x.startswith("Item__scoreContainer_")
                )
                if score_container:
                    item_info["score_container"] = score_container.get_text(strip=True)

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

    processador = info["top_container"].split("R$")[0].strip()

    price: str = "N/A"
    if "R$" in info["top_container"]:
        price = info["top_container"].split("R$")[1].split("_cpu")[0].strip()

    tipo: str = "N/A"
    if "_cpu" in info["name_and_props"]:
        tipo = info["name_and_props"].split("_cpu")[1].split("_nanometers")[0].strip()

    nanometros: str = "N/A"
    if "_nanometers" in info["name_and_props"]:
        nanometros = (
            info["name_and_props"]
            .split("_nanometers")[1]
            .split("nm_gauge_max_light")[0]
            .strip()
        )

    ghz: str = "N/A"
    if "nm_gauge_max_light" in info["name_and_props"]:
        ghz = (
            info["name_and_props"]
            .split("nm_gauge_max_light")[1]
            .split("GHz")[0]
            .strip()
        )

    score = info["score_container"].split("pontos")[0]

    print("Processador: ", processador)
    print("Preço: ", price)
    print("Tipo: ", tipo)
    print("Nanometros: ", nanometros)
    print("Ghz: ", ghz)
    print("Score: ", score, " \n")
    #
    # CPU.objects.create(
    #     nome=processador,
    #     pontuacao=score,
    #     preco=price,
    #     tipo=tipo,
    #     nanometros=nanometros,
    #     ghz=ghz,
    # )

print("Paginas percorridas: ", page)
