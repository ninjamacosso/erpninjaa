"""
Modelos do aplicativo accounts
"""
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    """Modelo de perfil do usuário"""
    ACCOUNT_TYPES = (
        ('personal', 'Pessoal'),
        ('business', 'Empresa')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField('Nome completo', max_length=100, blank=True)
    type = models.CharField('Tipo de conta', max_length=20, choices=ACCOUNT_TYPES, default='personal')
    phone = models.CharField('Telefone', max_length=20, blank=True)
    address = models.CharField('Endereço', max_length=200, blank=True)
    city = models.CharField('Cidade', max_length=100, blank=True)
    state = models.CharField('Estado', max_length=50, blank=True)
    country = models.CharField('País', max_length=50, blank=True)
    postal_code = models.CharField('Código Postal', max_length=20, blank=True)
    
    # Campos para empresas
    company_name = models.CharField('Nome da Empresa', max_length=100, blank=True)
    company_registration = models.CharField('CNPJ/NIF', max_length=50, blank=True)
    company_type = models.CharField('Tipo de Empresa', max_length=50, blank=True)
    industry = models.CharField('Setor de Atuação', max_length=100, blank=True)
    website = models.URLField('Website', blank=True)
    
    # Campos de controle
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return f'Perfil de {self.user.username}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Cria um perfil quando um usuário é criado"""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Salva o perfil quando o usuário é salvo"""
    instance.profile.save()
