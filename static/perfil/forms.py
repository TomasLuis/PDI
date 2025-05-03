from django import forms
from .models import Servico

class PerfilForm(forms.Form):
    email = forms.EmailField(label='Email')
    nome = forms.CharField(label='Nome', max_length=100)
    contacto = forms.CharField(label='Contacto', max_length=20)
    distrito = forms.CharField(label='Distrito', max_length=100)

class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['categoria', 'descricao', 'email', 'nome', 'contacto', 'distrito', 'informacoes_adicionais', 'foto']