from django.db import models

class GPU(models.Model):

    nome = models.CharField(max_length=200)
    pontuacao = models.FloatField(default=0)

    def __str__(self):
        return self.nome

class CPU(models.Model):

    nome = models.CharField(max_length=200)
    pontuacao = models.FloatField(default=0)

    def __str__(self):
        return self.nome
