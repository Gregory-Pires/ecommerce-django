from django.urls import path
from . import views

urlpatterns = [
    path('', views.loja, name='loja'),
    path('categoria/<slug:slug_categoria>/', views.loja, name='produtos_por_categoria'),
    path('categoria/<slug:slug_categoria>/<slug:slug_produto>', views.produto_detail, name='produto_detail'),
    path('pesquisa/', views.pesquisa, name='pesquisa'),
    path('enviar_avaliacao/<int:produto_id>', views.enviar_avaliacao, name='enviar_avaliacao'),
]