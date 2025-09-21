from django.urls import path
from . import views

urlpatterns = [
   path('fazer_pedido/', views.fazer_pedido, name='fazer_pedido'),
   path('pagamentos/', views.pagamentos, name='pagamentos'),
   path('pedido_completo/', views.pedido_completo, name='pedido_completo'),
]