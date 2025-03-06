"""
Formulários de autenticação
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models.user import User

class LoginForm(FlaskForm):
    """Formulário de login"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')

class RegistrationForm(FlaskForm):
    """Formulário de registro"""
    username = StringField('Nome de usuário', validators=[
        DataRequired(),
        Length(min=2, max=20)
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[
        DataRequired(),
        Length(min=6, message='A senha deve ter pelo menos 6 caracteres')
    ])
    password2 = PasswordField('Confirmar senha', validators=[
        DataRequired(),
        EqualTo('password', message='As senhas devem ser iguais')
    ])
    account_type = SelectField('Tipo de conta', choices=[
        ('personal', 'Pessoal'),
        ('business', 'Empresa')
    ], validators=[DataRequired()])
    submit = SubmitField('Registrar')

    def validate_username(self, username):
        """Valida se o nome de usuário já existe"""
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Este nome de usuário já está em uso.')

    def validate_email(self, email):
        """Valida se o email já existe"""
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Este email já está registrado.') 