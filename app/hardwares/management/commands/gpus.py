import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from utils.has_next_page import has_next_page
from hardwares.models import GPU


class Command(BaseCommand):
    help = "Obtém informações de GPUs e armazena no banco de dados"

    def handle(self, *args, **kwargs):
        url = "https://versus.com/br/graphics-card"
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
                            "div",
                            class_=lambda x: x and x.startswith("Item__topContainer_"),
                        )
                        if top_container:
                            item_info["top_container"] = top_container.get_text(
                                strip=True
                            )

                            name_and_props = top_container.find(
                                "div",
                                class_=lambda x: x
                                and x.startswith("Item__nameAndProps_"),
                            )
                            if name_and_props:
                                item_info["name_and_props"] = name_and_props.get_text(
                                    strip=True
                                )

                        score_container = item.find(
                            "div",
                            class_=lambda x: x
                            and x.startswith("Item__scoreContainer_"),
                        )
                        if score_container:
                            item_info["score_container"] = score_container.get_text(
                                strip=True
                            )

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
            placa_de_video = info["top_container"].split("R$")[0].strip()
            if "_gauge_max_light" in placa_de_video:
                placa_de_video = placa_de_video.split("_gauge_max_light")[0].strip()

            price: str = "N/A"
            if "R$" in info["top_container"]:
                price = info["top_container"].split("R$")[1].split("_cpu")[0].strip()

            if "_gauge_max_light" in price:
                price = f"R${price.split('_gauge_max_light')[0].strip()}"

            tflops: str = "N/A"
            if "_gauge_max_light" in info["top_container"]:
                tflops = (
                    info["top_container"]
                    .split("_gauge_max_light")[1]
                    .split("TFLOPS")[0]
                    .strip()
                )

            memoria: str = "N/A"
            if "_memory_light" in info["top_container"]:
                memoria = (
                    info["top_container"]
                    .split("_memory_light")[1]
                    .split("_pixel_rate")[0]
                    .strip()
                )

            gpixels: str = "N/A"
            if "_pixel_rate" in info["top_container"]:
                gpixels = info["top_container"].split("_pixel_rate")[1].strip()

            score = info["score_container"].split("pontos")[0].strip()

            self.stdout.write(f"Placa de vídeo: {placa_de_video}")
            self.stdout.write(f"Preço: {price}")
            self.stdout.write(f"TFLOPS: {tflops}")
            self.stdout.write(f"Memória: {memoria}")
            self.stdout.write(f"GPixels: {gpixels}")
            self.stdout.write(f"Pontuação: {score} \n")

            gpu, _ = GPU.objects.get_or_create(
                nome=placa_de_video,
            )

            gpu.pontuacao = score
            gpu.preco = price
            gpu.tflops = tflops
            gpu.memoria = memoria
            gpu.gpixels = gpixels
            gpu.save()

        self.stdout.write(self.style.SUCCESS(f"Paginas percorridas: {page}"))
