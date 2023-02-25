from django.apps import AppConfig


class PhoneLineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'phone_line'

    
    def ready(self) -> None:
        from . import signals
        return super().ready()
