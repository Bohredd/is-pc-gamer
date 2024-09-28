import re
import spacy
from django.core.management.base import BaseCommand
from hardwares.models import CPU, GPU
from app.upgradify.helpers import get_ram_value, calcular_nota_ram
from app.upgradify.settings import (
    MIN_CPU_SCORE,
    MIN_GPU_SCORE,
    RAM_HIERARCHY,
    MIN_RAM_SIZE,
    MIN_STORAGE_SIZE,
    RAM_HIERARCHY_MIN_SCORE,
    RAM_SIZE_SCORE,
    RAM_MIN_SCORE,
    PC_GAMER_MIN_SCORE,
)


class Command(BaseCommand):
    help = "Identifica os componentes de um texto dado"

    def add_arguments(self, parser):
        parser.add_argument(
            "texto", type=str, help="Texto para identificar componentes de hardware"
        )

    def handle(self, *args, **kwargs):
        texto = kwargs["texto"]

        notas = []
        avisos = []

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

        somatorio_pontuacao_pc = 0

        if cpus_encontradas:
            if len(cpus_encontradas) > 1:
                somatorio = 0
                for cpu in cpus_encontradas:
                    somatorio += CPU.objects.get(nome=cpu).pontuacao

                pontuacao = somatorio / len(cpus_encontradas)

                avisos.append("Mais de uma CPU encontrada.")
            else:
                pontuacao = CPU.objects.get(nome=cpus_encontradas[0]).pontuacao
            if pontuacao < MIN_CPU_SCORE:
                avisos.append("Pontuação da CPU abaixo do mínimo.")
            else:
                notas.append(f"CPU suficiente.")

            somatorio_pontuacao_pc += pontuacao
        else:
            avisos.append("Nenhuma CPU encontrada.")

        if gpus_encontradas:
            if len(gpus_encontradas) > 1:
                somatorio = 0
                for gpu in gpus_encontradas:
                    if isinstance(gpu, str):
                        somatorio += 0
                    else:
                        somatorio += gpu.pontuacao

                pontuacao = somatorio / len(gpus_encontradas)

                avisos.append("Mais de uma GPU encontrada.")
            else:
                if isinstance(gpus_encontradas[0], str):
                    pontuacao = 5
                else:
                    pontuacao = gpus_encontradas[0].pontuacao

            if pontuacao < MIN_GPU_SCORE:
                avisos.append("Pontuação da GPU abaixo do mínimo.")
            else:
                notas.append(f"GPU suficiente.")

            somatorio_pontuacao_pc += pontuacao
        else:
            avisos.append("Nenhuma GPU encontrada.")

        if "DDR" in texto:
            DDR_TEXTO = re.search(r"DDR\d", texto)

            if DDR_TEXTO:
                especificacao_ddr = DDR_TEXTO.group(0)

                memorias_ram = re.findall(r"\d+\s?GB", texto)

                if len(memorias_ram) > 1:

                    for memoria in memorias_ram:

                        if memoria in [gpu.memoria for gpu in gpus_encontradas]:
                            memorias_ram.remove(memoria)

                points_memory_ddr = get_ram_value(especificacao_ddr, RAM_HIERARCHY)

                # print("Memórias RAM:", memorias_ram)

                if len(memorias_ram) > 1:
                    memorias_ram = [memorias_ram[1]]

                nota_memoria_ram = calcular_nota_ram(
                    int(memorias_ram[0].split("GB")[0]), RAM_SIZE_SCORE
                )

                # print("Nota da Memória RAM:", nota_memoria_ram)
                somatorio_pontuacao_pc += nota_memoria_ram

                if nota_memoria_ram >= RAM_MIN_SCORE:

                    if points_memory_ddr >= RAM_HIERARCHY_MIN_SCORE:
                        notas.append(f"Memória RAM Suficiente")
                    else:
                        avisos.append("Velocidade da Memória RAM abaixo do mínimo.")
                else:
                    avisos.append("Tamanho da Memória RAM abaixo do mínimo.")

            print("Nota para PC Gamer:", somatorio_pontuacao_pc)
            print("Nota minimia para PC Gamer:", PC_GAMER_MIN_SCORE)
            if somatorio_pontuacao_pc >= PC_GAMER_MIN_SCORE:
                print("is a pc gamer")
            else:
                print("is not a pc gamer")
            print("Notas:", notas)
            print("Avisos:", avisos)
