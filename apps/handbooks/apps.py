from django.apps import AppConfig


class HandbooksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.handbooks'

    def ready(self):
        import apps.handbooks.signals
