"""
URLs do aplicativo core
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
] 