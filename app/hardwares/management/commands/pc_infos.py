import re
import spacy
from django.core.management.base import BaseCommand
from hardwares.models import CPU, GPU
from app.upgradify.helpers import get_ram_value
from app.upgradify.settings import (
    MIN_CPU_SCORE,
    MIN_GPU_SCORE,
    RAM_HIERARCHY,
    MIN_RAM_SIZE,
    MIN_STORAGE_SIZE,
)


class Command(BaseCommand):
    help = "Identifica os componentes de um texto dado"

    def add_arguments(self, parser):
        parser.add_argument(
            "texto", type=str, help="Texto para identificar componentes de hardware"
        )

    def handle(self, *args, **kwargs):
        texto = kwargs["texto"]

        cpus = CPU.objects.values_list("nome", flat=True)
        gpus = GPU.objects.all()

        graficos_integrados = ["Intel HD Graphics", "AMD Radeon Graphics"]
        cpus_set = set(cpus)

        cpus_encontradas = []
        gpus_encontradas = []

        especificacao_ddr = None

        for cpu in cpus_set:
            if cpu.lower() in texto.lower():
                cpus_encontradas.append(cpu)

        for gpu in gpus:
            if gpu.is_in_text(texto):
                gpus_encontradas.append(gpu)

        for grafico_integrado in graficos_integrados:
            if grafico_integrado.lower() in texto.lower():
                print("Encontrei o gráfico integrado:", grafico_integrado)
                gpus_encontradas.append(grafico_integrado)

        if cpus_encontradas:
            if len(cpus_encontradas) > 1:
                somatorio = 0
                for cpu in cpus_encontradas:
                    somatorio += CPU.objects.get(nome=cpu).pontuacao

                pontuacao = somatorio / len(cpus_encontradas)

                if pontuacao >= MIN_CPU_SCORE:
                    is_good = True
            else:
                pontuacao = CPU.objects.get(nome=cpus_encontradas[0]).pontuacao
        else:
            print("Nenhuma CPU encontrada.")

        print("Pontuação:", pontuacao)

        if gpus_encontradas:
            if len(gpus_encontradas) > 1:
                somatorio = 0
                for gpu in gpus_encontradas:
                    if isinstance(gpu, str):
                        somatorio += 0
                    else:
                        somatorio += gpu.pontuacao

                pontuacao = somatorio / len(gpus_encontradas)

                if pontuacao >= MIN_GPU_SCORE:
                    is_good = True
            else:
                pontuacao = gpus_encontradas[0].pontuacao
        else:
            print("Nenhuma GPU encontrada.")

        print("POntuação:", pontuacao)
        # TODO: Encontrar a quantidade de armazenamento

        if "DDR" in texto:
            DDR_TEXTO = re.search(r"DDR\d", texto)

            if DDR_TEXTO:
                especificacao_ddr = DDR_TEXTO.group(0)

                memorias_ram = re.findall(r"\d+\s?GB", texto)

                if len(memorias_ram) > 1:

                    for memoria in memorias_ram:

                        if memoria in [gpu.memoria for gpu in gpus_encontradas]:
                            memorias_ram.remove(memoria)

                    print("Memórias RAM restantes:", memorias_ram)

                points_memory_ddr = get_ram_value(especificacao_ddr, RAM_HIERARCHY)

                if int(memorias_ram[0].split("GB")[0]) >= MIN_RAM_SIZE:
                    is_good = True
                else:
                    is_good = False

                print("Pontos de memória:", points_memory_ddr)
                print("É suficiente?", is_good)
