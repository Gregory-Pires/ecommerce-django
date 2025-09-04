from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('ativar/<uidb64>/<token>/', views.ativar, name='ativar')

]