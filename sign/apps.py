from django.apps import AppConfig


class SignConfig(AppConfig):
    name = 'sign'

    def ready(self):
        import sign.signals
