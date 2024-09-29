import re
import requests
from bs4 import BeautifulSoup

# Sites aceitos para raspagem
sites_aceitos = [
    "kabum",
    "mercadolivre",
    "studiopc",
    "magazineluiza",
]

# Dicionário com os tipos e identificadores para os sites
onde_esta_informacoes = {
    "kabum": {
        "tipo": "id",
        "identificador": "technicalInfoSection",
    },
    "mercadolivre": {
        "tipo": "class_",
        "identificador": "ui-pdp-description__content",
    },
    "studiopc": {
        "tipo": "class_",
        "identificador": "h1 m-0",
    },
    "magazineluiza": {
        "tipo": "class_",
        "identificador": "sc-fqkvVR hlqElk sc-gazJty bndlSw",
    },
}


def get_info_tecnica(url):
    # Determinando qual site está sendo acessado
    site = None
    for s in sites_aceitos:
        if s in url:
            site = s
            break

    if not site:
        raise ValueError(
            "Site não suportado. Apenas 'kabum', 'mercadolivre', 'studiopc', e 'magazineluiza' são aceitos."
        )

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Levanta exceção para erros HTTP

        soup = BeautifulSoup(response.text, "html.parser")

        # Acessando a seção de informações técnicas conforme o site
        tipo = onde_esta_informacoes[site]["tipo"]
        identificador = onde_esta_informacoes[site]["identificador"]

        # Usando getattr para selecionar o método apropriado (id ou class_)
        info_tecnica = soup.find(**{tipo: identificador})

        if info_tecnica:
            return info_tecnica.get_text(strip=True)
        else:
            raise ValueError("A seção de informações técnicas não foi encontrada.")

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Erro ao fazer a requisição: {e}")


# Exemplo de uso
# url = "https://www.kabum.com.br/produto-exemplo"
# print(get_info_tecnica(url))
