from django.apps import AppConfig


class PostboardAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'postboard_app'

#добавим в единственный класс файла apps.py метод ready,
# который выполнится при завершении конфигурации нашего приложения newapp.
# В самом методе импортируем сигналы, таким образом зарегистрировав их.
    def ready(self):
        from . import signals  # выполнение модуля -> регистрация сигналов

