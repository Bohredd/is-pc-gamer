def get_ram_value(ram_key, RAM_HIERARCHY):
    for ram_dict in RAM_HIERARCHY:
        if ram_key in ram_dict:
            return ram_dict[ram_key]
    return None


def calcular_nota_ram(tamanho_ram, RAM_SIZE_SCORE):

    # Se o valor está exatamente nas chaves do dicionário, retorna a nota correspondente
    if tamanho_ram in RAM_SIZE_SCORE:
        return RAM_SIZE_SCORE[tamanho_ram]

    # Se o valor for maior que 32, retorna a nota máxima (100)
    if tamanho_ram > 32:
        return 100

    # Verifica os intervalos e atribui a nota correspondente
    notas = sorted(RAM_SIZE_SCORE.items())
    for i in range(len(notas) - 1):
        min_val, min_score = notas[i]
        max_val, max_score = notas[i + 1]

        # Se o valor está entre min_val e max_val
        if min_val < tamanho_ram < max_val:
            # Interpolação linear para calcular a nota proporcional
            score_interpolado = min_score + (tamanho_ram - min_val) * (
                max_score - min_score
            ) / (max_val - min_val)
            return round(score_interpolado)

    return (
        0  # Retorna 0 para valores fora do escopo (menores que o mínimo, por exemplo)
    )
