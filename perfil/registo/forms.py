from django import forms
from django.contrib.auth.models import User

class SignUpForm(forms.ModelForm):
    email = forms.EmailField(label="Email", required=True)
    password1 = forms.CharField(label="Senha", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar Senha", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "password1", "password2"]  # Apenas esses campos

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email  # Define o username como o email
        user.set_password(self.cleaned_data["password1"])  # Define a senha corretamente
        if commit:
            user.save()
        return user
