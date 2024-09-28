from django.db import models


class GPU(models.Model):

    nome = models.CharField(max_length=200, unique=True)
    pontuacao = models.FloatField(default=None, blank=True, null=True)
    preco = models.CharField(max_length=200, default=None, blank=True, null=True)
    tflops = models.CharField(max_length=200, default=None, blank=True, null=True)
    memoria = models.CharField(max_length=200, default=None, blank=True, null=True)
    gpixels = models.CharField(max_length=200, default=None, blank=True, null=True)

    identifier = models.CharField(max_length=200, default=None, blank=True, null=True)

    def __str__(self):
        return self.identifier

    def is_in_text(self, text: str) -> bool:
        return self.identifier.lower() in text.lower()

    def is_dedicated(self) -> bool:
        # TODO
        return True

    def is_integrated(self) -> bool:
        # TODO
        return False

    def save(self, *args, **kwargs):

        if "GB" not in self.nome or "MB" not in self.nome:
            if self.memoria in self.nome:
                pass
            else:
                self.identifier = f"{self.nome} {self.memoria}"
        else:
            self.identifier = self.nome

        if "Laptop" in self.identifier or "Notebook" in self.identifier:
            self.identifier = self.identifier.replace("Laptop", "")
            self.identifier = self.identifier.replace("Notebook", "")

        super(GPU, self).save(*args, **kwargs)


class CPU(models.Model):

    nome = models.CharField(max_length=200, unique=True)
    pontuacao = models.FloatField(max_length=200, default=None, blank=True, null=True)
    preco = models.CharField(max_length=200, default=None, blank=True, null=True)
    tipo = models.CharField(max_length=15, default="N/A", blank=True, null=True)
    nanometros = models.CharField(max_length=200, default=None, blank=True, null=True)
    ghz = models.CharField(max_length=200, default=None, blank=True, null=True)

    def __str__(self):
        return self.nome
