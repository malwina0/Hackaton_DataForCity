from django.apps import AppConfig


class SmogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'smog'

    def ready(self):
        from .scheduler import scheduler
        scheduler.start()
