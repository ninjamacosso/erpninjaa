from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from .models import (
    Funcionario, Departamento, FolhaPagamento, 
    Ferias, Cargo, BeneficioFuncionario, Beneficio,
    FaltaLicenca, HoraExtra, Treinamento, DocumentoRH
)

# Dashboard
@login_required
def rh_dashboard(request):
    hoje = timezone.now().date()
    mes_atual = hoje.month
    ano_atual = hoje.year
    
    # Total de funcionários ativos
    total_funcionarios = Funcionario.objects.filter(status='A').count()
    
    # Folha de pagamento do mês atual
    folha_pagamento_total = FolhaPagamento.objects.filter(
        mes_referencia=mes_atual,
        ano_referencia=ano_atual
    ).aggregate(total=Sum('valor_liquido'))['total'] or 0
    
    # Funcionários em férias
    funcionarios_ferias = Ferias.objects.filter(
        data_inicio__lte=hoje,
        data_fim__gte=hoje,
        status='EM_ANDAMENTO'
    ).count()
    
    # Aniversariantes do mês
    aniversariantes = Funcionario.objects.filter(
        data_nascimento__month=mes_atual,
        status='A'
    ).count()
    
    # Dados para o gráfico de departamentos
    departamentos = Departamento.objects.annotate(
        total_funcionarios=Count('funcionario')
    )
    departamentos_labels = [dep.nome for dep in departamentos]
    departamentos_data = [dep.total_funcionarios for dep in departamentos]
    
    # Dados para o gráfico de evolução
    meses = []
    evolucao_data = []
    for i in range(12, -1, -1):
        data = hoje - timedelta(days=i*30)
        meses.append(data.strftime('%b/%Y'))
        evolucao_data.append(
            Funcionario.objects.filter(
                data_admissao__lte=data,
                status='A'
            ).count()
        )
    
    # Últimas contratações
    ultimas_contratacoes = Funcionario.objects.filter(
        status='A'
    ).order_by('-data_admissao')[:5]
    
    # Próximas férias
    proximas_ferias = Ferias.objects.filter(
        data_inicio__gte=hoje,
        status='AGENDADA'
    ).order_by('data_inicio')[:5]
    
    context = {
        'total_funcionarios': total_funcionarios,
        'folha_pagamento_total': folha_pagamento_total,
        'funcionarios_ferias': funcionarios_ferias,
        'aniversariantes': aniversariantes,
        'departamentos_labels': departamentos_labels,
        'departamentos_data': departamentos_data,
        'evolucao_labels': meses,
        'evolucao_data': evolucao_data,
        'ultimas_contratacoes': ultimas_contratacoes,
        'proximas_ferias': proximas_ferias,
    }
    
    return render(request, 'rh/dashboard.html', context)

# Funcionários
@login_required
def funcionarios_list(request):
    funcionarios = Funcionario.objects.all()
    return render(request, 'rh/funcionarios/list.html', {'funcionarios': funcionarios})

@login_required
def funcionario_create(request):
    if request.method == 'POST':
        # Implementar lógica de criação
        pass
    return render(request, 'rh/funcionarios/form.html')

@login_required
def funcionario_detail(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    return render(request, 'rh/funcionarios/detail.html', {'funcionario': funcionario})

@login_required
def funcionario_update(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    if request.method == 'POST':
        # Implementar lógica de atualização
        pass
    return render(request, 'rh/funcionarios/form.html', {'funcionario': funcionario})

# Folha de Pagamento
@login_required
def folha_pagamento_list(request):
    folhas = FolhaPagamento.objects.all().order_by('-ano_referencia', '-mes_referencia')
    return render(request, 'rh/folha_pagamento/list.html', {'folhas': folhas})

@login_required
def folha_pagamento_create(request):
    if request.method == 'POST':
        # Implementar lógica de criação
        pass
    return render(request, 'rh/folha_pagamento/form.html')

@login_required
def folha_pagamento_detail(request, pk):
    folha = get_object_or_404(FolhaPagamento, pk=pk)
    return render(request, 'rh/folha_pagamento/detail.html', {'folha': folha})

@login_required
def folha_pagamento_gerar(request):
    if request.method == 'POST':
        # Implementar lógica de geração
        pass
    return render(request, 'rh/folha_pagamento/gerar.html')

# Benefícios
@login_required
def beneficios_list(request):
    beneficios = Beneficio.objects.all()
    return render(request, 'rh/beneficios/list.html', {'beneficios': beneficios})

@login_required
def beneficio_create(request):
    if request.method == 'POST':
        # Implementar lógica de criação
        pass
    return render(request, 'rh/beneficios/form.html')

@login_required
def beneficio_detail(request, pk):
    beneficio = get_object_or_404(Beneficio, pk=pk)
    return render(request, 'rh/beneficios/detail.html', {'beneficio': beneficio})

@login_required
def beneficio_update(request, pk):
    beneficio = get_object_or_404(Beneficio, pk=pk)
    if request.method == 'POST':
        # Implementar lógica de atualização
        pass
    return render(request, 'rh/beneficios/form.html', {'beneficio': beneficio})

# Férias
@login_required
def ferias_list(request):
    ferias = Ferias.objects.all().order_by('-data_inicio')
    return render(request, 'rh/ferias/list.html', {'ferias': ferias})

@login_required
def ferias_create(request):
    if request.method == 'POST':
        # Implementar lógica de criação
        pass
    return render(request, 'rh/ferias/form.html')

@login_required
def ferias_detail(request, pk):
    ferias = get_object_or_404(Ferias, pk=pk)
    return render(request, 'rh/ferias/detail.html', {'ferias': ferias})

@login_required
def ferias_update(request, pk):
    ferias = get_object_or_404(Ferias, pk=pk)
    if request.method == 'POST':
        # Implementar lógica de atualização
        pass
    return render(request, 'rh/ferias/form.html', {'ferias': ferias})

# Faltas e Licenças
@login_required
def faltas_licencas_list(request):
    faltas = FaltaLicenca.objects.all().order_by('-data_inicio')
    return render(request, 'rh/faltas_licencas/list.html', {'faltas': faltas})

@login_required
def falta_licenca_create(request):
    if request.method == 'POST':
        # Implementar lógica de criação
        pass
    return render(request, 'rh/faltas_licencas/form.html')

@login_required
def falta_licenca_detail(request, pk):
    falta = get_object_or_404(FaltaLicenca, pk=pk)
    return render(request, 'rh/faltas_licencas/detail.html', {'falta': falta})

# Horas Extras
@login_required
def horas_extras_list(request):
    horas = HoraExtra.objects.all().order_by('-data')
    return render(request, 'rh/horas_extras/list.html', {'horas': horas})

@login_required
def hora_extra_create(request):
    if request.method == 'POST':
        # Implementar lógica de criação
        pass
    return render(request, 'rh/horas_extras/form.html')

@login_required
def hora_extra_detail(request, pk):
    hora = get_object_or_404(HoraExtra, pk=pk)
    return render(request, 'rh/horas_extras/detail.html', {'hora': hora})

# Cargos e Salários
@login_required
def cargos_list(request):
    cargos = Cargo.objects.all()
    return render(request, 'rh/cargos/list.html', {'cargos': cargos})

@login_required
def cargo_create(request):
    if request.method == 'POST':
        # Implementar lógica de criação
        pass
    return render(request, 'rh/cargos/form.html')

@login_required
def cargo_detail(request, pk):
    cargo = get_object_or_404(Cargo, pk=pk)
    return render(request, 'rh/cargos/detail.html', {'cargo': cargo})

@login_required
def cargo_update(request, pk):
    cargo = get_object_or_404(Cargo, pk=pk)
    if request.method == 'POST':
        # Implementar lógica de atualização
        pass
    return render(request, 'rh/cargos/form.html', {'cargo': cargo})

# Recrutamento
@login_required
def vagas_list(request):
    return render(request, 'rh/recrutamento/list.html')

@login_required
def vaga_create(request):
    if request.method == 'POST':
        # Implementar lógica de criação
        pass
    return render(request, 'rh/recrutamento/form.html')

@login_required
def vaga_detail(request, pk):
    return render(request, 'rh/recrutamento/detail.html')

# Treinamentos
@login_required
def treinamentos_list(request):
    treinamentos = Treinamento.objects.all().order_by('-data_inicio')
    return render(request, 'rh/treinamentos/list.html', {'treinamentos': treinamentos})

@login_required
def treinamento_create(request):
    if request.method == 'POST':
        # Implementar lógica de criação
        pass
    return render(request, 'rh/treinamentos/form.html')

@login_required
def treinamento_detail(request, pk):
    treinamento = get_object_or_404(Treinamento, pk=pk)
    return render(request, 'rh/treinamentos/detail.html', {'treinamento': treinamento})

# Documentos
@login_required
def documentos_list(request):
    documentos = DocumentoRH.objects.all().order_by('-data_upload')
    return render(request, 'rh/documentos/list.html', {'documentos': documentos})

@login_required
def documento_create(request):
    if request.method == 'POST':
        # Implementar lógica de criação
        pass
    return render(request, 'rh/documentos/form.html')

@login_required
def documento_detail(request, pk):
    documento = get_object_or_404(DocumentoRH, pk=pk)
    return render(request, 'rh/documentos/detail.html', {'documento': documento}) 