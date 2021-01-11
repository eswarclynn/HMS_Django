from django.apps import AppConfig


class InstituteConfig(AppConfig):
    name = 'institute'

    def ready(self):
        import institute.signals
