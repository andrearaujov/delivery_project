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
]