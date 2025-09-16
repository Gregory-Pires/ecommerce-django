from django.urls import path
from . import views

urlpatterns = [
   path('fazer_pedido/', views.fazer_pedido, name='fazer_pedido'),
]