from django.apps import AppConfig

class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hsabackend'

    # if you create a new signal, make sure to add it here!!!
    def ready(self):
        from hsabackend.signalhandlers import password_reset_signal