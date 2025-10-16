from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.RestauranteListView.as_view(), name='lista_restaurantes'),
    path('restaurante/<int:pk>/', views.RestauranteDetailView.as_view(), name='detalhe_restaurante'),
    path('adicionar-ao-carrinho/,<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/', views.ver_carrinho, name='ver_carrinho'),
]