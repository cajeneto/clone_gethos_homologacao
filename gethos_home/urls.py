from django.contrib import admin
from django.urls import path
from django.http import HttpResponse


#  importando da views do app
from gethos_home.views import (
    home,
    create_account,
    dashboard_auth,
    logout_view,
    login_admin,
    importar_contatos
    
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"), #trata do login do usuário
    path("painelCentralUser/", dashboard_auth, name="dashboard_auth"), #trata do painel após autenticação do login do usuário.
    path("login_admin/", login_admin, name="login_admin"),
    path("criarContaGethos", create_account, name="create_account"),
    path("logoutUser/", logout_view, name="logout_view"), #trata do logout do usuário
    path('importar-contatos/', importar_contatos, name='importar_contatos'),
]
