from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'apps.users'

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'

    def ready(self):
        import apps.users.signals
