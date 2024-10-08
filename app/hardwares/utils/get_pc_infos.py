import re
from hardwares.models import CPU, GPU
from upgradify.helpers import get_ram_value, calcular_nota_ram, avaliar_pc_pela_nota
from upgradify.settings import (
    MIN_CPU_SCORE,
    MIN_GPU_SCORE,
    RAM_HIERARCHY,
    RAM_HIERARCHY_MIN_SCORE,
    RAM_SIZE_SCORE,
    RAM_MIN_SCORE,
    PC_GAMER_MIN_SCORE,
    PONTUACOES_PC_GAMER,
)


def identificar_componentes_hardware(texto):

    print("Texto: " + texto)

    notas = []
    avisos = []

    cpus = CPU.objects.values_list("nome", flat=True)
    gpus = GPU.objects.all()

    graficos_integrados = ["Intel HD Graphics", "AMD Radeon Graphics", "Radeon Vega 7"]
    cpus_set = set(cpus)

    cpus_encontradas = []
    gpus_encontradas = []

    especificacao_ddr = None

    # Identifica CPUs no texto
    for cpu in cpus_set:
        if cpu.lower() in texto.lower():
            cpus_encontradas.append(cpu)

    if not cpus_encontradas:
        remocoes_nome = ["NVIDIA", "GeForce", "AMD", "Radeon"]

        for cpu in cpus_set:
            nome = cpu.lower()
            for remocao in remocoes_nome:
                nome = nome.replace(remocao.lower(), "").strip()
            if nome in texto.lower():
                cpus_encontradas.append(cpu)

    # Identifica GPUs no texto
    for gpu in gpus:
        if gpu.is_in_text(texto):
            gpus_encontradas.append(gpu)
        elif gpu.nome.lower() in texto.lower():
            gpus_encontradas.append(gpu)

    if not gpus_encontradas:
        remocoes_nome = [
            "NVIDIA",
            "AMD",
            "Radeon",
            "Laptop",
        ]

        for gpu in gpus:
            nome = gpu.nome

            # print("Nome: " + nome)

            for remocao in remocoes_nome:
                nome = nome.replace(remocao.lower(), "").strip()

            if nome.lower() in texto.lower():
                print("Nome: " + nome)

                for cpu in cpus_encontradas:

                    if cpu.lower() in nome.lower():
                        pass
                    else:
                        gpus_encontradas.append(gpu)

    # Tratamento para GPUs não encontradas retirando memórias
    if not gpus_encontradas:
        remocoes_nome = [
            "NVIDIA",
            "AMD",
            "Radeon",
            "Laptop",
        ]

        for gpu in gpus:
            nome = gpu.nome

            for remocao in remocoes_nome:
                nome = nome.lower().replace(remocao.lower(), "").strip()
                nome = nome.lower().replace("gddr", "").strip()
                for i in range(0, 50):
                    nome = nome.replace(f"{str(i)}gb", "").strip()
                    nome = nome.replace(f"{str(i)} gb", "").strip()

            if "rtx 3060" in nome:
                print("Nome: " + nome)

                print("Texto: " + texto)

            if nome.lower().strip() in texto.lower():
                print("Nome: " + nome)

                for cpu in cpus_encontradas:

                    if cpu.lower() in nome.lower():
                        pass
                    else:
                        gpus_encontradas.append(gpu)

    # Verifica gráficos integrados
    for grafico_integrado in graficos_integrados:
        if grafico_integrado.lower() in texto.lower():
            gpus_encontradas.append(grafico_integrado)
            avisos.append("Gráfico integrado encontrado.")

            for gpu in gpus_encontradas:
                if gpu not in graficos_integrados:
                    gpus_encontradas.remove(gpu)

    somatorio_pontuacao_pc = 0

    # Avalia CPUs encontradas
    if cpus_encontradas:
        if len(cpus_encontradas) > 1:
            somatorio = sum(
                CPU.objects.get(nome=cpu).pontuacao for cpu in cpus_encontradas
            )
            pontuacao = somatorio / len(cpus_encontradas)
            avisos.append("Mais de uma CPU encontrada.")
        else:
            pontuacao = CPU.objects.get(nome=cpus_encontradas[0]).pontuacao

        if pontuacao < MIN_CPU_SCORE:
            avisos.append("Pontuação da CPU abaixo do mínimo.")
        else:
            notas.append("CPU suficiente.")

        somatorio_pontuacao_pc += pontuacao
    else:
        avisos.append("Nenhuma CPU encontrada.")

    # Avalia GPUs encontradas
    if gpus_encontradas:
        if len(gpus_encontradas) > 1:
            somatorio = sum(
                gpu.pontuacao if isinstance(gpu, GPU) else 0 for gpu in gpus_encontradas
            )
            pontuacao = somatorio / len(gpus_encontradas)
            avisos.append("Mais de uma GPU encontrada.")
        else:
            pontuacao = (
                gpus_encontradas[0].pontuacao
                if isinstance(gpus_encontradas[0], GPU)
                else 5
            )

        if pontuacao < MIN_GPU_SCORE:
            avisos.append("Pontuação da GPU abaixo do mínimo.")
        else:
            notas.append("GPU suficiente.")

        somatorio_pontuacao_pc += pontuacao
    else:
        avisos.append("Nenhuma GPU encontrada.")

    memorias_ram = []

    if "DDR" in texto:
        DDR_TEXTO = re.search(r"DDR\d", texto)
        if DDR_TEXTO:
            especificacao_ddr = DDR_TEXTO.group(0)
            memorias_ram = re.findall(r"\d+\s?GB", texto)

            points_memory_ddr = get_ram_value(especificacao_ddr, RAM_HIERARCHY)

            if len(memorias_ram) > 1:

                arrumado = False
                for i in range(len(memorias_ram)):
                    texto_antes, texto_pos = texto.split(memorias_ram[i])

                    for j in range(len(memorias_ram)):

                        if "ram" in texto_pos.lower():
                            outras_memorias_presentes = any(
                                m in texto_pos
                                for m in memorias_ram
                                if m != memorias_ram[j]
                            )

                            if not outras_memorias_presentes:

                                memorias_ram = [memorias_ram[j]]
                                arrumado = True
                                break

                    if arrumado:
                        break

                memorias_ram = [min(int(ram.replace("GB", "")) for ram in memorias_ram)]
                memorias_ram = [f"{memorias_ram[0]}GB"]

            nota_memoria_ram = calcular_nota_ram(
                int(memorias_ram[0].split("GB")[0]), RAM_SIZE_SCORE
            )
            somatorio_pontuacao_pc += nota_memoria_ram

            if nota_memoria_ram >= RAM_MIN_SCORE:
                if points_memory_ddr >= RAM_HIERARCHY_MIN_SCORE:
                    notas.append("Memória RAM suficiente e Velocidade suficiente.")
                else:
                    avisos.append("Velocidade da Memória RAM abaixo do mínimo.")
            else:
                avisos.append("Tamanho da Memória RAM abaixo do mínimo.")

    avaliacao_pc = avaliar_pc_pela_nota(somatorio_pontuacao_pc, PONTUACOES_PC_GAMER)

    return {
        "somatorio_pontuacao_pc": somatorio_pontuacao_pc,
        "notas": notas,
        "avisos": avisos,
        "avaliacao_pc": avaliacao_pc,
    }, {
        "cpus_encontradas": cpus_encontradas,
        "gpus_encontradas": gpus_encontradas,
        "especificacao_ddr": especificacao_ddr,
        "memorias_ram": memorias_ram,
    }
