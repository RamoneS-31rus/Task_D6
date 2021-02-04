from django.apps import AppConfig


class NewsConfig(AppConfig):
    name = 'news'

    def ready(self): # нам надо переопределить метод ready, чтобы при готовности нашего приложения импортировался модуль со всеми
        import news.signals