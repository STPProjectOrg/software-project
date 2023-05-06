from django.apps import AppConfig


class ApiAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_app'

    # Um den scheduler zu starten nachdem das Projekt vollständig initialisiert wurde,
    # muss die Methode ready() überschrieben werden.
    # Leider muss der Import vom scheduler hier stehen, da es sonst zu einem Zirkulären Import kommt.
    def ready(self):
        from .scheduler import start_scheduler
        start_scheduler()
