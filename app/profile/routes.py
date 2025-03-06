"""
Rotas de perfil
"""
from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.profile import bp
from app.profile.forms import ProfileForm
from app import db

@bp.route('/view')
@login_required
def view():
    """Visualizar perfil"""
    return render_template('profile/view.html', title='Meu Perfil')

@bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    """Editar perfil"""
    form = ProfileForm()
    if form.validate_on_submit():
        profile = current_user.profile
        profile.name = form.name.data
        profile.phone = form.phone.data
        profile.address = form.address.data
        profile.city = form.city.data
        profile.state = form.state.data
        profile.country = form.country.data
        profile.postal_code = form.postal_code.data
        
        if profile.type == 'business':
            profile.company_name = form.company_name.data
            profile.company_registration = form.company_registration.data
            profile.company_type = form.company_type.data
            profile.industry = form.industry.data
            profile.website = form.website.data
        
        profile.is_complete = True
        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('profile.view'))
    
    elif request.method == 'GET':
        profile = current_user.profile
        form.name.data = profile.name
        form.phone.data = profile.phone
        form.address.data = profile.address
        form.city.data = profile.city
        form.state.data = profile.state
        form.country.data = profile.country
        form.postal_code.data = profile.postal_code
        
        if profile.type == 'business':
            form.company_name.data = profile.company_name
            form.company_registration.data = profile.company_registration
            form.company_type.data = profile.company_type
            form.industry.data = profile.industry
            form.website.data = profile.website
    
    return render_template('profile/edit.html', title='Editar Perfil', form=form) 