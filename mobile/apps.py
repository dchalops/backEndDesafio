from django.apps import AppConfig
import os


class MobileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mobile'
    path = os.path.dirname(os.path.abspath(__file__))


