from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100, blank=True, null=True)
    contacto = models.CharField(max_length=20, blank=True, null=True)
    distrito = models.CharField(max_length=100, blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', null=True, blank=True)

    def __str__(self):
        return self.user.username

class Servico(models.Model):
    categoria = models.CharField(max_length=100)
    descricao = models.TextField()
    email = models.EmailField()
    nome = models.CharField(max_length=100)
    contacto = models.CharField(max_length=20)
    distrito = models.CharField(max_length=100)
    informacoes_adicionais = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to='servicos/', blank=True, null=True)
    prestador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='servicos_prestados')

    def __str__(self):
        return self.categoria

class Classificacao(models.Model):
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, related_name='classificacoes')
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classificacoes_feitas')
    classificacao = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Classificação de 1 a 5
    comentario = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Classificação de {self.cliente.username} para {self.servico.nome}"