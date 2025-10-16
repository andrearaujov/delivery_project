# core/admin.py

from django.contrib import admin
from .models import Cliente, Restaurante, Produto, Pedido, ItemPedido, Entrega, Avaliacao

# A forma mais simples de registrar os modelos
admin.site.register(Cliente)
admin.site.register(Restaurante)
admin.site.register(Produto)
admin.site.register(Pedido)
admin.site.register(ItemPedido)
admin.site.register(Entrega)
admin.site.register(Avaliacao)