"""
Views do aplicativo core
"""
from django.shortcuts import render

def home(request):
    """Página inicial"""
    return render(request, 'core/home.html')
