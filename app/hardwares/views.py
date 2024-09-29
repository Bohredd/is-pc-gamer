from django.shortcuts import render
from .forms import AvaliacaoForms
from .utils.get_pc_infos import (
    identificar_componentes_hardware,
)


def home(request):
    return render(request, "hardwares/home.html")


def avaliador(request):
    resultado_avaliacao = None
    if request.method == "POST":
        form = AvaliacaoForms(request.POST)

        print(form.errors)
        if form.is_valid():
            texto = form.cleaned_data["texto"]
            resultado_avaliacao = identificar_componentes_hardware(texto)
            print(resultado_avaliacao)
    else:
        form = AvaliacaoForms()

    return render(
        request,
        "hardwares/avaliador.html",
        {
            "form": form,
            "resultado_avaliacao": resultado_avaliacao,
        },
    )


def login(request):
    return render(request, "hardwares/login.html")


def cadastro(request):
    return render(request, "hardwares/cadastro.html")
