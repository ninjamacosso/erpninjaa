from django.apps import AppConfig

class RHConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rh'
    verbose_name = 'Recursos Humanos'

    def ready(self):
        import rh.signals  # noqa 