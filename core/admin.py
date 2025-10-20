# core/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Cliente, Restaurante, Produto, Pedido, ItemPedido, Entrega, Avaliacao

# Define um "inline" para o modelo Cliente.
class ClienteInline(admin.StackedInline):
    model = Cliente
    can_delete = False
    verbose_name_plural = 'Perfil do Cliente'
    fields = ('telefone', 'endereco', 'tipo_usuario')

# Define uma nova classe UserAdmin que inclui o ClienteInline
class UserAdmin(BaseUserAdmin):
    inlines = (ClienteInline,)

# Define uma classe para customizar a exibição do Restaurante
class RestauranteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo_cozinha', 'dono')
    list_filter = ('dono',)
    search_fields = ('nome', 'tipo_cozinha')

# A ordem aqui é importante: primeiro cancela, depois registra de novo.
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Registra os outros modelos
admin.site.register(Restaurante, RestauranteAdmin)
admin.site.register(Produto)
admin.site.register(Pedido)
admin.site.register(ItemPedido)
admin.site.register(Entrega)
admin.site.register(Avaliacao)