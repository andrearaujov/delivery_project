from django import forms
from django.contrib.auth.models import User

class CadastroForm(forms.ModelForm):
    # Campos extras que não estão no modelo User padrão
    telefone = forms.CharField(max_length=15, required=True)
    endereco = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = User
        # Campos que queremos do modelo User
        fields = ('username', 'email', 'password')
        # Usamos um widget para que o campo de senha não mostre o texto digitado
        widgets = {
            'password': forms.PasswordInput(),
        }