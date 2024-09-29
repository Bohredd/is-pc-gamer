from django.shortcuts import render
from .forms import AvaliacaoForms
from .models import CPU, GPU
from .utils.get_pc_infos import (
    identificar_componentes_hardware,
)
from .utils.get_text_anuncio import get_info_tecnica
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string


def home(request):
    return render(request, "hardwares/home.html")


def avaliador(request):
    resultado_avaliacao = None
    componentes_encontrados = None
    if request.method == "POST":
        form = AvaliacaoForms(request.POST)

        print(form.errors)
        if form.is_valid():
            texto = form.cleaned_data["texto"]
            if not texto:
                texto = get_info_tecnica(form.cleaned_data["url"])
            resultado_avaliacao, componentes_encontrados = (
                identificar_componentes_hardware(texto)
            )
            print("Componentes encontrados:" + str(componentes_encontrados))
            print(resultado_avaliacao)
    else:
        form = AvaliacaoForms()

    return render(
        request,
        "hardwares/avaliador.html",
        {
            "form": form,
            "resultado_avaliacao": resultado_avaliacao,
            "componentes_encontrados": componentes_encontrados,
        },
    )


def login(request):
    return render(request, "hardwares/login.html")


def cadastro(request):
    return render(request, "hardwares/cadastro.html")


def base(request):
    return render(request, "hardwares/base.html")


def htmx_busca_dados_formulario_hardwares(request):
    # Obtém o valor da pesquisa do parâmetro GET
    query = request.GET.get("search", "")

    # Filtra CPUs com base na consulta
    cpus = CPU.objects.filter(Q(nome__icontains=query)) if query else CPU.objects.all()

    # Filtra GPUs com base na consulta
    gpus = (
        GPU.objects.filter(Q(nome__icontains=query) | Q(identifier__icontains=query))
        if query
        else GPU.objects.all()
    )

    # Limita a 10 resultados e conta o total de resultados
    cpu_results = cpus[:10]
    gpu_results = gpus[:10]

    total_cpu_results = cpus.count()
    total_gpu_results = gpus.count()

    results_html = "".join(
        f'<div data-id="{cpu.id}">{cpu.nome}</div>' for cpu in cpu_results
    ) + "".join(
        f'<div data-id="{gpu.id}">{gpu.nome} (ID: {gpu.identifier})</div>'
        for gpu in gpu_results
    )

    # Adiciona "Ver mais" se houver mais resultados
    if total_cpu_results > 10 or total_gpu_results > 10:
        more_count = (
            total_cpu_results + total_gpu_results - 20
        )  # Total de resultados além de 10
        results_html += f'<div data-id="ver_mais" class="text-primary cursor-pointer">Ver mais ({more_count})</div>'

    # Retorna a resposta HTTP com o HTML gerado
    return HttpResponse(results_html)


def ver_mais_hardwares(request):
    # Obtém o valor da pesquisa do parâmetro GET
    query = request.GET.get("search", "")
    offset = int(
        request.GET.get("offset", 0)
    )  # Obtém o offset para paginar os resultados

    # Filtra CPUs com base na consulta
    cpus = CPU.objects.filter(Q(nome__icontains=query)) if query else CPU.objects.all()

    # Filtra GPUs com base na consulta
    gpus = (
        GPU.objects.filter(Q(nome__icontains=query) | Q(identifier__icontains=query))
        if query
        else GPU.objects.all()
    )

    # Limita os resultados com base no offset e adiciona mais 10
    cpu_results = cpus[offset : offset + 10]
    gpu_results = gpus[offset : offset + 10]

    # Renderiza um template com os resultados
    context = {
        "cpu_results": cpu_results,
        "gpu_results": gpu_results,
        "query": query,
    }
    return render(request, "hardwares/vermais.html", context)
