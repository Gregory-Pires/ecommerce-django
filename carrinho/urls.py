from django.urls import path
from . import views

urlpatterns = [
    path('', views.carrinho, name='carrinho'),
    path('add_carrinho/<int:produto_id>/', views.add_carrinho, name='add_carrinho'),
]