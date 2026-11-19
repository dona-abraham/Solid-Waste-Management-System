from django.apps import AppConfig

class SwmappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'swmapp'

    def ready(self):
        import swmapp.signals  # Use the actual app name here
