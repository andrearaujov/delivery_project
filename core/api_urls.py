from django.urls import path
from . import api_views

urlpatterns = [
    path('restaurantes/', api_views.restaurant_list_api, name='api_restaurant_list'),
    path('restaurantes/<int:pk>/', api_views.restaurant_detail_api, name='api_restaurant_detail'),
    path('login/', api_views.login_api, name='api_login'),
    path('logout/', api_views.logout_api, name='api_logout'),
    path('user/', api_views.user_info_api, name='api_user_info'),
    path('carrinho/', api_views.cart_api, name='api_cart'),
    path('carrinho/adicionar/', api_views.add_to_cart_api, name='api_add_to_cart'),
    path('checkout/', api_views.checkout_api, name='api_checkout'),
]
