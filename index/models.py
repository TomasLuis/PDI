from django.db import models

class Especialista(models.Model):
    nome = models.CharField(max_length=200)
    categoria = models.CharField(max_length=100)
    classificacao = models.FloatField()
    imagem = models.ImageField(upload_to='especialistas/')
    descricao = models.CharField(max_length=100)
    def __str__(self):
        return self.nome
    


class Servico(models.Model):
    categoria = models.CharField(max_length=100, verbose_name="Categoria do Serviço")
    descricao = models.TextField(verbose_name="Descrição do Serviço", blank=True, null=True)
    email = models.EmailField(verbose_name="Email de Contacto", blank=True, null=True)
    nome = models.CharField(max_length=255, verbose_name="Nome do Prestador")
    contacto = models.CharField(max_length=20, verbose_name="Contacto Telefónico", blank=True, null=True)
    distrito = models.CharField(max_length=100, verbose_name="Distrito", blank=True, null=True)
    informacoes_adicionais = models.TextField(verbose_name="Informações Adicionais", blank=True, null=True)
    foto = models.ImageField(upload_to='servicos/', verbose_name="Foto do Serviço", blank=True, null=True)
    prestador = models.ForeignKey('perfil.Perfil', on_delete=models.CASCADE, verbose_name="Prestador de Serviço")