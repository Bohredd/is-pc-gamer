from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("avaliador/", views.avaliador, name="avaliador"),
    path("login/", views.login, name="login"),
    path("cadastro/", views.cadastro, name="cadastro"),
    path("base/", views.base, name="base"),
    path(
        "htmx-busca-dados-formulario-hardwares/",
        views.htmx_busca_dados_formulario_hardwares,
        name="htmx_busca_dados_formulario_hardwares",
    ),
    path("ver-mais/", views.ver_mais_hardwares, name="ver_mais_resultados"),
]
