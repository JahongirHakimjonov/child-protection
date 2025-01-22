from django.apps import AppConfig


class MobileConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.mobile"

    def ready(self):
        import apps.mobile.signals  # noqa
