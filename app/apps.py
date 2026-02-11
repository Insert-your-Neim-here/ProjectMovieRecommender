from django.apps import AppConfig


class MyAppConfig(AppConfig):  # Renamed class to MyAppConfig
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"
