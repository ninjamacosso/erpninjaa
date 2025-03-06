"""
URLs do aplicativo dashboard
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('vendas/', views.vendas, name='vendas'),
    path('estoque/', views.estoque, name='estoque'),
    path('clientes/', views.clientes, name='clientes'),
    path('fornecedores/', views.fornecedores, name='fornecedores'),
    path('relatorios/', views.relatorios, name='relatorios'),
] 