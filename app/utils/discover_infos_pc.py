import re


def identificar_componentes(texto):
    componentes = {"processador": None, "placa_video": None, "memoria_ram": None}

    # Expressões regulares para identificar os componentes
    processador_regex = r"(Intel\s*Core\s*i\d|\s*AMD\s*Ryzen\s*\d+|Intel\s*Pentium|Intel\s*Celeron|AMD\s*Athlon|Xeon|Threadripper|Core\s*i\d+|Ryzen\s*Threadripper)"
    placa_video_regex = r"(NVIDIA\s*GeForce\s*(RTX|GTX)?\s*\d+\s*(\d+GB)?|AMD\s*Radeon\s*(RX|Vega)?\s*\d+\s*(\d+GB)?|Intel\s*HD\s*Graphics|Vega|Arc)"
    memoria_ram_regex = r"(\d+\s?GB\s?(DDR\d|RAM))"

    # Procurar Processador
    processador = re.search(processador_regex, texto, re.IGNORECASE)
    if processador:
        componentes["processador"] = processador.group(0).strip()

    # Procurar Placa de Vídeo
    placa_video = re.search(placa_video_regex, texto, re.IGNORECASE)
    if placa_video:
        componentes["placa_video"] = placa_video.group(0).strip()

    # Procurar Memória RAM
    memoria_ram = re.search(memoria_ram_regex, texto, re.IGNORECASE)
    if memoria_ram:
        componentes["memoria_ram"] = memoria_ram.group(0)

    return componentes


# Exemplo de uso
texto = """
Este computador vem equipado com um Processador Intel Core i7 de última geração, 
uma placa de vídeo NVIDIA GeForce RTX 3060 4GB e 16 GB DDR4 de Memória RAM.
"""

componentes_identificados = identificar_componentes(texto)
print(componentes_identificados)
