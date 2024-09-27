from django.db import models


class GPU(models.Model):

    nome = models.CharField(max_length=200)
    pontuacao = models.FloatField(default=0)
    preco = models.FloatField(default=0)
    tflops = models.FloatField(default=0)
    memoria = models.FloatField(default=0)
    gpixels = models.FloatField(default=0)

    def __str__(self):
        return self.nome


class CPU(models.Model):

    nome = models.CharField(max_length=200)
    pontuacao = models.FloatField(default=0)
    preco = models.FloatField(default=0)
    tipo = models.CharField(max_length=15, default="N/A")
    nanometros = models.FloatField(default=0)
    ghz = models.FloatField(default=0)

    def __str__(self):
        return self.nome
