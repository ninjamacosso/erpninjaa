"""
Rotas de autenticação
"""
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from werkzeug.urls import url_parse
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models.user import User
from app.models.profile import Profile
from app import db

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Email ou senha inválidos', 'error')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Login', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Página de registro"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        
        # Criar perfil inicial
        profile = Profile(
            user=user,
            type=form.account_type.data
        )
        
        db.session.add(user)
        db.session.add(profile)
        db.session.commit()
        
        flash('Parabéns, você agora está registrado!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Registro', form=form)

@bp.route('/logout')
def logout():
    """Rota de logout"""
    logout_user()
    return redirect(url_for('main.index')) 