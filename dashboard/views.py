"""
Views do aplicativo dashboard
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """Página principal do dashboard"""
    return render(request, 'dashboard/index.html')

@login_required
def vendas(request):
    """Página de vendas"""
    return render(request, 'dashboard/vendas.html')

@login_required
def estoque(request):
    """Página de estoque"""
    return render(request, 'dashboard/estoque.html')

@login_required
def clientes(request):
    """Página de clientes"""
    return render(request, 'dashboard/clientes.html')

@login_required
def fornecedores(request):
    """Página de fornecedores"""
    return render(request, 'dashboard/fornecedores.html')

@login_required
def relatorios(request):
    """Página de relatórios"""
    return render(request, 'dashboard/relatorios.html')
