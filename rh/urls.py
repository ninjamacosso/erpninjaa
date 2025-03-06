from django.urls import path
from . import views

app_name = 'rh'

urlpatterns = [
    # Dashboard
    path('', views.rh_dashboard, name='rh_dashboard'),
    
    # Funcionários
    path('funcionarios/', views.funcionarios_list, name='funcionarios'),
    path('funcionarios/novo/', views.funcionario_create, name='funcionario_create'),
    path('funcionarios/<int:pk>/', views.funcionario_detail, name='funcionario_detail'),
    path('funcionarios/<int:pk>/editar/', views.funcionario_update, name='funcionario_update'),
    
    # Folha de Pagamento
    path('folha-pagamento/', views.folha_pagamento_list, name='folha_pagamento'),
    path('folha-pagamento/nova/', views.folha_pagamento_create, name='folha_pagamento_create'),
    path('folha-pagamento/<int:pk>/', views.folha_pagamento_detail, name='folha_pagamento_detail'),
    path('folha-pagamento/gerar/', views.folha_pagamento_gerar, name='folha_pagamento_gerar'),
    
    # Benefícios
    path('beneficios/', views.beneficios_list, name='beneficios'),
    path('beneficios/novo/', views.beneficio_create, name='beneficio_create'),
    path('beneficios/<int:pk>/', views.beneficio_detail, name='beneficio_detail'),
    path('beneficios/<int:pk>/editar/', views.beneficio_update, name='beneficio_update'),
    
    # Férias
    path('ferias/', views.ferias_list, name='ferias'),
    path('ferias/nova/', views.ferias_create, name='ferias_create'),
    path('ferias/<int:pk>/', views.ferias_detail, name='ferias_detail'),
    path('ferias/<int:pk>/editar/', views.ferias_update, name='ferias_update'),
    
    # Faltas e Licenças
    path('faltas-licencas/', views.faltas_licencas_list, name='faltas_licencas'),
    path('faltas-licencas/nova/', views.falta_licenca_create, name='falta_licenca_create'),
    path('faltas-licencas/<int:pk>/', views.falta_licenca_detail, name='falta_licenca_detail'),
    
    # Horas Extras
    path('horas-extras/', views.horas_extras_list, name='horas_extras'),
    path('horas-extras/nova/', views.hora_extra_create, name='hora_extra_create'),
    path('horas-extras/<int:pk>/', views.hora_extra_detail, name='hora_extra_detail'),
    
    # Cargos e Salários
    path('cargos-salarios/', views.cargos_list, name='cargos_salarios'),
    path('cargos-salarios/novo/', views.cargo_create, name='cargo_create'),
    path('cargos-salarios/<int:pk>/', views.cargo_detail, name='cargo_detail'),
    path('cargos-salarios/<int:pk>/editar/', views.cargo_update, name='cargo_update'),
    
    # Recrutamento
    path('recrutamento/', views.vagas_list, name='recrutamento'),
    path('recrutamento/nova-vaga/', views.vaga_create, name='vaga_create'),
    path('recrutamento/<int:pk>/', views.vaga_detail, name='vaga_detail'),
    
    # Treinamentos
    path('treinamentos/', views.treinamentos_list, name='treinamentos'),
    path('treinamentos/novo/', views.treinamento_create, name='treinamento_create'),
    path('treinamentos/<int:pk>/', views.treinamento_detail, name='treinamento_detail'),
    
    # Documentos
    path('documentos/', views.documentos_list, name='documentos_rh'),
    path('documentos/novo/', views.documento_create, name='documento_create'),
    path('documentos/<int:pk>/', views.documento_detail, name='documento_detail'),
] 