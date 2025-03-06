"""
URLs do aplicativo financeiro
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='financeiro'),
    path('receita/nova/', views.nova_receita, name='nova_receita'),
    path('despesa/nova/', views.nova_despesa, name='nova_despesa'),
    path('categoria/nova/', views.nova_categoria, name='nova_categoria'),
    path('dados/', views.dados_financeiros, name='dados_financeiros'),
] 