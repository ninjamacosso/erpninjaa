"""
Views do aplicativo financeiro
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """Página principal do módulo financeiro"""
    return render(request, 'financeiro/index.html')

@login_required
def nova_receita(request):
    """Criar nova receita"""
    return render(request, 'financeiro/nova_receita.html')

@login_required
def nova_despesa(request):
    """Criar nova despesa"""
    return render(request, 'financeiro/nova_despesa.html')

@login_required
def nova_categoria(request):
    """Criar nova categoria"""
    return render(request, 'financeiro/nova_categoria.html')

@login_required
def dados_financeiros(request):
    """Retorna dados financeiros para os gráficos"""
    return render(request, 'financeiro/dados_financeiros.html')
