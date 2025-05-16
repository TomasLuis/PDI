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
        fields = ['categoria', 'descricao', 'foto', 'email', 'nome', 'contacto', 'distrito', 'informacoes_adicionais']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['foto'].widget = forms.FileInput()

    def clean_foto(self):
        foto = self.cleaned_data.get('foto')
        if not foto:
            raise forms.ValidationError("É obrigatório colocar foto no serviço.")
        return foto