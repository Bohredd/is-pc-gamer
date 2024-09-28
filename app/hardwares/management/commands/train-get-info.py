import spacy
from hardwares.models import GPU, CPU
import re

# Carregando o modelo SpaCy
nlp = spacy.load("en_core_web_sm")


def identificar_componentes_ia(texto):
    componentes = {"processador": None, "placa_video": None, "memoria_ram": None}

    # Processar o texto com SpaCy
    doc = nlp(texto)

    # Extrair os nomes de CPU e GPU do banco de dados Django
    cpus = CPU.objects.values_list("nome", flat=True)
    gpus = GPU.objects.values_list("nome", flat=True)

    # Função auxiliar para encontrar a melhor correspondência de CPU e GPU
    def encontrar_melhor_correspondencia(entidades, banco_de_dados):
        melhor_correspondencia = None
        for entidade in entidades:
            for componente in banco_de_dados:
                if entidade.text.lower() in componente.lower():
                    melhor_correspondencia = componente
                    break
        return melhor_correspondencia

    # Procurar entidades nomeadas no texto
    cpus_entidades = [entidade for entidade in doc.ents if entidade.label_ == "PRODUCT"]
    gpus_entidades = [entidade for entidade in doc.ents if entidade.label_ == "PRODUCT"]

    # Identificar processador
    componentes["processador"] = encontrar_melhor_correspondencia(cpus_entidades, cpus)

    # Identificar placa de vídeo
    componentes["placa_video"] = encontrar_melhor_correspondencia(gpus_entidades, gpus)

    # Identificar Memória RAM (ajustando diretamente do texto usando regex)
    memoria_ram_regex = r"(\d+\s?GB\s?(DDR\d|RAM))"
    memoria_ram = re.search(memoria_ram_regex, texto, re.IGNORECASE)
    if memoria_ram:
        componentes["memoria_ram"] = memoria_ram.group(0)

    return componentes


# Exemplo de uso

texto = """
Este computador vem equipado com um Processador Intel Core i7-2600K de última geração, 
uma placa de vídeo NVIDIA GeForce RTX 3060 4GB e 16 GB DDR4 de Memória RAM.
"""

componentes_identificados = identificar_componentes_ia(texto)
print(componentes_identificados)
