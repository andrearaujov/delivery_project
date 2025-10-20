# core/models.py

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User  
# -----------------------------------------------------------------------------
# Entidade: Cliente
# -----------------------------------------------------------------------------
class Cliente(models.Model):
    # 1. DEFININDO AS OPÇÕES DE TIPO DE USUÁRIO
    TIPO_USUARIO_CHOICES = [
        ('CLIENTE', 'Cliente'),
        ('RESTAURANTE', 'Dono de Restaurante'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=15)
    endereco = models.TextField()
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES, default='CLIENTE')

    def __str__(self):
        return self.user.username

# -----------------------------------------------------------------------------
# Entidade: Restaurante
# -----------------------------------------------------------------------------
class Restaurante(models.Model):
   
    dono = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurantes')
    
    nome = models.CharField(max_length=100)
    endereco = models.TextField()
    horario_funcionamento = models.CharField(max_length=100, help_text="Ex: 08:00-22:00")
    tipo_cozinha = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

# -----------------------------------------------------------------------------
# Entidade: Produto
# -----------------------------------------------------------------------------
class Produto(models.Model):
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, related_name='produtos')
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=50, help_text="Ex: Entrada, Prato Principal, Sobremesa")
    # Para o ImageField funcionar, é necessário instalar a biblioteca Pillow:
    # pip install Pillow
    foto = models.ImageField(upload_to='produtos_fotos/', blank=True, null=True)

    def __str__(self):
        return f"{self.nome} - {self.restaurante.nome}"

# -----------------------------------------------------------------------------
# Entidade: Pedido
# -----------------------------------------------------------------------------
class Pedido(models.Model):
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Em preparação', 'Em preparação'),
        ('A caminho', 'A caminho'),
        ('Entregue', 'Entregue'),
        ('Cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, related_name='pedidos')
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, related_name='pedidos')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pendente')
    data_pedido = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nome if self.cliente else 'Cliente Excluído'}"

# -----------------------------------------------------------------------------
# Tabela Associativa: ItemPedido (Conecta Pedido e Produto)
# -----------------------------------------------------------------------------
class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} no Pedido #{self.pedido.id}"

# -----------------------------------------------------------------------------
# Entidade: Entrega
# -----------------------------------------------------------------------------
class Entrega(models.Model):
    # OneToOneField garante que um pedido SÓ pode ter UMA entrega
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, primary_key=True)
    tempo_estimado = models.CharField(max_length=50, help_text="Ex: 30-45 min")
    
    def __str__(self):
        return f"Entrega para o Pedido #{self.pedido.id}"

# -----------------------------------------------------------------------------
# Entidade: Avaliacao
# -----------------------------------------------------------------------------
class Avaliacao(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, related_name='avaliacoes')
    nota = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comentario = models.TextField(blank=True, null=True)
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação de {self.cliente.nome} para {self.restaurante.nome}: Nota {self.nota}"