from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('painel/', views.painel, name='painel'),
    path('', views.painel, name='painel'),


    path('ativar/<uidb64>/<token>/', views.ativar, name='ativar'),
    path('esqueceusuasenha/', views.esqueceusuasenha, name='esqueceusuasenha'),
    path('resetsenha_validate/<uidb64>/<token>/', views.resetsenha_validate, name='resetsenha_validate'),
    path('resetsenha/', views.resetsenha, name='resetsenha'),

    path('meus_pedidos/', views.meus_pedidos, name='meus_pedidos'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
]