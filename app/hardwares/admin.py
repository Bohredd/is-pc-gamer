from django.contrib import admin
from .models import GPU, CPU


class GPUAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "pontuacao",
        "preco",
        "tflops",
        "memoria",
        "gpixels",
        "identifier",
    )
    list_filter = (
        "nome",
        "pontuacao",
        "preco",
        "tflops",
        "memoria",
        "gpixels",
        "identifier",
    )
    search_fields = (
        "nome",
        "pontuacao",
        "preco",
        "tflops",
        "memoria",
        "gpixels",
        "identifier",
    )
    ordering = ("pontuacao",)


class CPUAdmin(admin.ModelAdmin):
    list_display = ("nome", "pontuacao", "preco", "tipo", "nanometros", "ghz")
    list_filter = ("nome", "pontuacao", "preco", "tipo", "nanometros", "ghz")
    search_fields = ("nome", "pontuacao", "preco", "tipo", "nanometros", "ghz")
    ordering = ("pontuacao",)


admin.site.register(CPU, CPUAdmin)
admin.site.register(GPU, GPUAdmin)
