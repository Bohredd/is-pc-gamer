import spacy
import re
from django.core.management.base import BaseCommand
from hardwares.models import CPU, GPU


class Command(BaseCommand):
    help = "Identifica os componentes de um texto dado"

    def add_arguments(self, parser):
        parser.add_argument(
            "texto", type=str, help="Texto para identificar componentes de hardware"
        )

    def handle(self, *args, **kwargs):
        texto = kwargs["texto"]

        # Carregar modelo SpaCy para português
        nlp = spacy.load("pt_core_news_sm")

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
        cpus_entidades = [
            entidade for entidade in doc.ents if entidade.label_ == "PRODUTO"
        ]
        gpus_entidades = [
            entidade for entidade in doc.ents if entidade.label_ == "PRODUTO"
        ]

        # Identificar processador
        componentes["processador"] = encontrar_melhor_correspondencia(
            cpus_entidades, cpus
        )

        # Identificar placa de vídeo
        componentes["placa_video"] = encontrar_melhor_correspondencia(
            gpus_entidades, gpus
        )

        # Identificar Memória RAM (ajustando diretamente do texto usando regex)
        memoria_ram_regex = r"(\d+\s?GB\s?(DDR\d|RAM))"
        memoria_ram = re.search(memoria_ram_regex, texto, re.IGNORECASE)
        if memoria_ram:
            componentes["memoria_ram"] = memoria_ram.group(0)

        # Exibir os resultados
        self.stdout.write(
            self.style.SUCCESS(f"Componentes identificados: {componentes}")
        )
