"""
Formulários do aplicativo accounts
"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    """Formulário de registro de usuário"""
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    """Formulário de atualização de usuário"""
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    """Formulário de atualização de perfil"""
    class Meta:
        model = Profile
        fields = ['name', 'phone', 'address', 'city', 'state', 'country', 'postal_code']
        if Profile._meta.get_field('type').get_default() == 'business':
            fields.extend(['company_name', 'company_registration', 'company_type', 'industry', 'website']) 