from django import forms
from django.contrib.auth.models import User
from .models import Cliente
from .models import Restaurante, Produto

class CadastroForm(forms.ModelForm):
    tipo_usuario = forms.ChoiceField(choices=Cliente.TIPO_USUARIO_CHOICES, required=True)
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
    
class RestauranteForm(forms.ModelForm):
    class Meta:
        model = Restaurante
        # O campo 'dono' será preenchido automaticamente pela view
        fields = ['nome', 'endereco', 'horario_funcionamento', 'tipo_cozinha']
        
        
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        # O campo 'restaurante' será preenchido automaticamente pela view
        fields = ['nome', 'descricao', 'preco', 'categoria', 'foto']
        
        
        
        