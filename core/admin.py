# core/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Cliente, Restaurante, Produto, Pedido, ItemPedido, Entrega, Avaliacao

class ClienteInline(admin.StackedInline):
    model = Cliente
    can_delete = False
    verbose_name_plural = 'clientes'
    
class UserAdmin(BaseUserAdmin):
    inline=(ClienteInline,)
    
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
    
# A forma mais simples de registrar os modelos
admin.site.register(Restaurante)
admin.site.register(Produto)
admin.site.register(Pedido)
admin.site.register(ItemPedido)
admin.site.register(Entrega)
admin.site.register(Avaliacao)