from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

#  importando da views do app
from gethos_home.views import home, create_account, dashboard_auth, login_admin, login_user, register_menssage_user, console_status_menssage_user, register_contacts_user


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login_user/', login_user, name='login_user'),
    path('login_admin/', login_admin, name='login_admin'),
    path('', home, name='home'),
    path('criarContaGethos', create_account, name='create_account'),
    path('painelCentralUser/', dashboard_auth, name='dashboard_auth'),
    path('login_user/register_contacts_user/', register_contacts_user, name='register_contacts_user'),
    path('login_user/register_menssage_user/', register_menssage_user, name='login_user/register_menssage_user'),
    path('login_user/register_menssage_user/console_status_menssage_user', console_status_menssage_user, name='console_status_menssage_user'),
]
