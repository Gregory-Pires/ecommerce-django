from django.urls import path
from . import views

urlpatterns = [
    path('', views.carrinho, name='carrinho'),
    path('add_carrinho/<int:produto_id>/', views.add_carrinho, name='add_carrinho'),
    path('remover_carrinho/<int:produto_id>/<int:carrinho_item_id>/', views.remover_carrinho, name='remover_carrinho'),
    path('remover_carrinho_item/<int:produto_id>/<int:carrinho_item_id>/', views.remover_carrinho_item, name='remover_carrinho_item'),

]