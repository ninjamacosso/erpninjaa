"""
Formulários de perfil
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, URL, Optional

class ProfileForm(FlaskForm):
    """Formulário de perfil"""
    # Campos básicos
    name = StringField('Nome completo', validators=[DataRequired(), Length(min=3, max=100)])
    phone = StringField('Telefone', validators=[DataRequired(), Length(min=9, max=20)])
    address = StringField('Endereço', validators=[DataRequired(), Length(max=200)])
    city = StringField('Cidade', validators=[DataRequired(), Length(max=100)])
    state = StringField('Estado', validators=[DataRequired(), Length(max=50)])
    country = StringField('País', validators=[DataRequired(), Length(max=50)])
    postal_code = StringField('Código Postal', validators=[DataRequired(), Length(max=20)])
    
    # Campos para empresas
    company_name = StringField('Nome da Empresa', validators=[Optional(), Length(max=100)])
    company_registration = StringField('CNPJ/NIF', validators=[Optional(), Length(max=50)])
    company_type = SelectField('Tipo de Empresa', choices=[
        ('', 'Selecione...'),
        ('ltda', 'Sociedade Limitada'),
        ('sa', 'Sociedade Anônima'),
        ('mei', 'Microempreendedor Individual'),
        ('ei', 'Empresário Individual'),
        ('other', 'Outro')
    ], validators=[Optional()])
    industry = StringField('Setor de Atuação', validators=[Optional(), Length(max=100)])
    website = StringField('Website', validators=[Optional(), URL()])
    
    submit = SubmitField('Salvar') 