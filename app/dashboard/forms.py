"""
Formulários do dashboard
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, DateField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class ReceitaForm(FlaskForm):
    """Formulário de receita"""
    descricao = StringField('Descrição', validators=[
        DataRequired(),
        Length(min=3, max=200)
    ])
    valor = DecimalField('Valor', validators=[DataRequired()])
    data = DateField('Data', validators=[DataRequired()])
    categoria = SelectField('Categoria', validators=[DataRequired()])
    forma_pagamento = SelectField('Forma de Pagamento', choices=[
        ('', 'Selecione'),
        ('dinheiro', 'Dinheiro'),
        ('pix', 'PIX'),
        ('cartao', 'Cartão'),
        ('boleto', 'Boleto')
    ], validators=[DataRequired()])
    observacoes = TextAreaField('Observações', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Salvar')

    def __init__(self, *args, **kwargs):
        super(ReceitaForm, self).__init__(*args, **kwargs)
        from app.models import Categoria
        self.categoria.choices = [
            (c.id, c.nome) for c in Categoria.query.filter_by(tipo='receita').order_by('nome')
        ]

class DespesaForm(FlaskForm):
    """Formulário de despesa"""
    descricao = StringField('Descrição', validators=[
        DataRequired(),
        Length(min=3, max=200)
    ])
    valor = DecimalField('Valor', validators=[DataRequired()])
    data = DateField('Data', validators=[DataRequired()])
    categoria = SelectField('Categoria', validators=[DataRequired()])
    forma_pagamento = SelectField('Forma de Pagamento', choices=[
        ('', 'Selecione'),
        ('dinheiro', 'Dinheiro'),
        ('pix', 'PIX'),
        ('cartao', 'Cartão'),
        ('boleto', 'Boleto')
    ], validators=[DataRequired()])
    observacoes = TextAreaField('Observações', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Salvar')

    def __init__(self, *args, **kwargs):
        super(DespesaForm, self).__init__(*args, **kwargs)
        from app.models import Categoria
        self.categoria.choices = [
            (c.id, c.nome) for c in Categoria.query.filter_by(tipo='despesa').order_by('nome')
        ]

class CategoriaForm(FlaskForm):
    """Formulário de categoria"""
    nome = StringField('Nome', validators=[
        DataRequired(),
        Length(min=3, max=50)
    ])
    tipo = SelectField('Tipo', choices=[
        ('receita', 'Receita'),
        ('despesa', 'Despesa')
    ], validators=[DataRequired()])
    descricao = TextAreaField('Descrição', validators=[Optional(), Length(max=200)])
    submit = SubmitField('Salvar') 