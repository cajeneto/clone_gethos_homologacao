
from django.contrib import admin
from django.urls import path, include

#  importando da views do app
from gethos_home.views import home, login_admin, login_user, register_menssage_user, console_status_menssage_user, register_contacts_user


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gethos_home.urls'))
]
