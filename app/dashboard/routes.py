"""
Rotas do dashboard
"""
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app.dashboard import bp
from app.dashboard.forms import ReceitaForm, DespesaForm, CategoriaForm
from app.models import Categoria, Receita, Despesa
from app import db

@bp.route('/')
@login_required
def index():
    """Página principal do dashboard"""
    return render_template('dashboard/index.html', title='Dashboard')

@bp.route('/vendas')
@login_required
def vendas():
    """Página de vendas"""
    return render_template('dashboard/vendas.html', title='Vendas')

@bp.route('/financeiro')
@login_required
def financeiro():
    """Página financeira"""
    receita_form = ReceitaForm()
    despesa_form = DespesaForm()
    
    # Buscar lançamentos do usuário
    receitas = Receita.query.filter_by(user_id=current_user.id).order_by(Receita.data.desc()).all()
    despesas = Despesa.query.filter_by(user_id=current_user.id).order_by(Despesa.data.desc()).all()
    
    # Calcular totais
    total_receitas = sum(float(r.valor) for r in receitas)
    total_despesas = sum(float(d.valor) for d in despesas)
    saldo = total_receitas - total_despesas
    
    return render_template('dashboard/financeiro.html',
                         title='Financeiro',
                         receita_form=receita_form,
                         despesa_form=despesa_form,
                         receitas=receitas,
                         despesas=despesas,
                         total_receitas=total_receitas,
                         total_despesas=total_despesas,
                         saldo=saldo)

@bp.route('/financeiro/receita/nova', methods=['POST'])
@login_required
def nova_receita():
    """Criar nova receita"""
    form = ReceitaForm()
    if form.validate_on_submit():
        receita = Receita(
            descricao=form.descricao.data,
            valor=form.valor.data,
            data=form.data.data,
            categoria_id=form.categoria.data,
            forma_pagamento=form.forma_pagamento.data,
            observacoes=form.observacoes.data,
            user_id=current_user.id
        )
        db.session.add(receita)
        db.session.commit()
        flash('Receita registrada com sucesso!', 'success')
        return redirect(url_for('dashboard.financeiro'))
    
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'Erro no campo {getattr(form, field).label.text}: {error}', 'error')
    return redirect(url_for('dashboard.financeiro'))

@bp.route('/financeiro/despesa/nova', methods=['POST'])
@login_required
def nova_despesa():
    """Criar nova despesa"""
    form = DespesaForm()
    if form.validate_on_submit():
        despesa = Despesa(
            descricao=form.descricao.data,
            valor=form.valor.data,
            data=form.data.data,
            categoria_id=form.categoria.data,
            forma_pagamento=form.forma_pagamento.data,
            observacoes=form.observacoes.data,
            user_id=current_user.id
        )
        db.session.add(despesa)
        db.session.commit()
        flash('Despesa registrada com sucesso!', 'success')
        return redirect(url_for('dashboard.financeiro'))
    
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'Erro no campo {getattr(form, field).label.text}: {error}', 'error')
    return redirect(url_for('dashboard.financeiro'))

@bp.route('/financeiro/categoria/nova', methods=['POST'])
@login_required
def nova_categoria():
    """Criar nova categoria"""
    form = CategoriaForm()
    if form.validate_on_submit():
        categoria = Categoria(
            nome=form.nome.data,
            tipo=form.tipo.data,
            descricao=form.descricao.data
        )
        db.session.add(categoria)
        db.session.commit()
        flash('Categoria criada com sucesso!', 'success')
        return redirect(url_for('dashboard.financeiro'))
    
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'Erro no campo {getattr(form, field).label.text}: {error}', 'error')
    return redirect(url_for('dashboard.financeiro'))

@bp.route('/financeiro/dados', methods=['GET'])
@login_required
def dados_financeiros():
    """Retorna dados financeiros para os gráficos"""
    # Buscar dados dos últimos 6 meses
    receitas = Receita.query.filter_by(user_id=current_user.id).order_by(Receita.data.desc()).limit(6).all()
    despesas = Despesa.query.filter_by(user_id=current_user.id).order_by(Despesa.data.desc()).limit(6).all()
    
    # Formatar dados para o gráfico
    dados = {
        'labels': [],
        'receitas': [],
        'despesas': []
    }
    
    # Adicionar dados mês a mês
    for i in range(5, -1, -1):
        mes = datetime.now().month - i
        ano = datetime.now().year
        if mes <= 0:
            mes += 12
            ano -= 1
        
        # Adicionar label do mês
        dados['labels'].append(f'{mes}/{ano}')
        
        # Calcular total de receitas do mês
        total_receitas = sum(float(r.valor) for r in receitas if r.data.month == mes and r.data.year == ano)
        dados['receitas'].append(total_receitas)
        
        # Calcular total de despesas do mês
        total_despesas = sum(float(d.valor) for d in despesas if d.data.month == mes and d.data.year == ano)
        dados['despesas'].append(total_despesas)
    
    return jsonify(dados)

@bp.route('/estoque')
@login_required
def estoque():
    """Página de estoque"""
    return render_template('dashboard/estoque.html', title='Estoque')

@bp.route('/clientes')
@login_required
def clientes():
    """Página de clientes"""
    return render_template('dashboard/clientes.html', title='Clientes')

@bp.route('/fornecedores')
@login_required
def fornecedores():
    """Página de fornecedores"""
    return render_template('dashboard/fornecedores.html', title='Fornecedores')

@bp.route('/relatorios')
@login_required
def relatorios():
    """Página de relatórios"""
    return render_template('dashboard/relatorios.html', title='Relatórios') 