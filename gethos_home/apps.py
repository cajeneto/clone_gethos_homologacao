from django.apps import AppConfig


# class GethosHomeConfig(AppConfig):
#     default_auto_field = "django.db.models.BigAutoField"
#     name = "gethos_home"
# # 

class GethosHomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gethos_home'

    def ready(self):
        import gethos_home.signals 