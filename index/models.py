from django.db import models

class Especialista(models.Model):
    nome = models.CharField(max_length=200)
    categoria = models.CharField(max_length=100)
    classificacao = models.FloatField()
    imagem = models.ImageField(upload_to='especialistas/')
    descricao = models.CharField(max_length=100)
    def __str__(self):
        return self.nome