from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

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

    def __str__(self):
        return self.nome


class Avaliacao(models.Model):
    servico = models.ForeignKey('Servico', on_delete=models.CASCADE, related_name='avaliacoes')
    classificacao = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Classificação"
    )
    comentario = models.TextField(blank=True, null=True, verbose_name="Comentário")
    data_avaliacao = models.DateTimeField(auto_now_add=True, verbose_name="Data da Avaliação")

    def __str__(self):
        return f"Avaliação de {self.servico.nome} - {self.classificacao} estrelas"
    
def avaliacao_media(self):
        """Calcula a avaliação média do serviço."""
        resultado = self.avaliacoes.aggregate(Avg('classificacao'))['classificacao__avg']
        return resultado if resultado else 0

def num_avaliacoes(self):
        """Calcula o número de avaliações do serviço."""
        return self.avaliacoes.count()

