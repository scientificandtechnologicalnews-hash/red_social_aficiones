from django.apps import AppConfig

class SocialConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'social'

    def ready(self):
        # Importamos el archivo de señales cuando la app esté cargada
        import social.signals