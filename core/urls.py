from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.RestauranteListView.as_view(), name='lista_restaurantes'),
    path('restaurante/<int:pk>/', views.RestauranteDetailView.as_view(), name='detalhe_restaurante'),
    path('adicionar-ao-carrinho/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),    path('carrinho/', views.ver_carrinho, name='ver_carrinho'),
    path('finalizar-pedido/', views.finalizar_pedido, name='finalizar_pedido'),
    path('pedido-confirmado/<int:pedido_id>/', views.pedido_confirmado, name='pedido_confirmado'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('meus-pedidos/', views.meus_pedidos, name='meus_pedidos'),
    path('painel/', views.painel_restaurante, name='painel_restaurante'),
    path('cadastrar-restaurante/', views.cadastrar_restaurante, name='cadastrar_restaurante'),
    path('painel/cardapio/', views.gerenciar_cardapio, name='gerenciar_cardapio'),
    path('painel/cardapio/adicionar/', views.adicionar_produto, name='adicionar_produto'),
    path('painel/cardapio/editar/<int:produto_id>/', views.editar_produto, name='editar_produto'),
    path('painel/cardapio/excluir/<int:produto_id>/', views.excluir_produto, name='excluir_produto'),
    path('painel/pedidos/', views.ver_pedidos_restaurante, name='ver_pedidos_restaurante'),
    path('painel/pedidos/atualizar-status/<int:pedido_id>/', views.atualizar_status_pedido, name='atualizar_status_pedido'),
]