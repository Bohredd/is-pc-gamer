from django.db import models


class GPU(models.Model):

    nome = models.CharField(max_length=200, unique=True)
    pontuacao = models.FloatField(default=None, blank=True, null=True)
    preco = models.CharField(max_length=200, default=None, blank=True, null=True)
    tflops = models.CharField(max_length=200, default=None, blank=True, null=True)
    memoria = models.CharField(max_length=200, default=None, blank=True, null=True)
    gpixels = models.CharField(max_length=200, default=None, blank=True, null=True)

    def __str__(self):
        return self.nome


class CPU(models.Model):

    nome = models.CharField(max_length=200, unique=True)
    pontuacao = models.FloatField(max_length=200, default=None, blank=True, null=True)
    preco = models.CharField(max_length=200, default=None, blank=True, null=True)
    tipo = models.CharField(max_length=15, default="N/A", blank=True, null=True)
    nanometros = models.CharField(max_length=200, default=None, blank=True, null=True)
    ghz = models.CharField(max_length=200, default=None, blank=True, null=True)

    def __str__(self):
        return self.nome
