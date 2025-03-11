from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.urls import path
from .views import enviar_mensagem_whatsapp  # Certifique-se de importar a view

# from .views import ContatoListCreate, ContatoDetail



#  importando da views do app
from gethos_home.views import (
    home,
    create_account,
    dashboard_auth,
    logout_view,
    login_admin,
    importar_contatos,
    salvar_dados_no_banco,
    enviar_mensagem_whatsapp,
    ContatoListCreate,
    ContatoDetail,
    CampanhaListCreateView,
   
    
    
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"), #trata do login do usuário
    path("painelCentralUser/", dashboard_auth, name="dashboard_auth"), #trata do painel após autenticação do login do usuário.
    path("login_admin/", login_admin, name="login_admin"),
    path("criarContaGethos", create_account, name="create_account"),
    path("logoutUser/", logout_view, name="logout_view"), #trata do logout do usuário
    path('importar-contatos/', importar_contatos, name='importar_contatos'),
    path("salvar_dados/", salvar_dados_no_banco, name="salvar_dados"),
    path('enviar-mensagem-whatsapp/', enviar_mensagem_whatsapp, name='enviar_mensagem_whatsapp'),
    path('api/contatos/', ContatoListCreate.as_view(), name='contato-list'),
    path('api/contatos/<int:pk>/', ContatoDetail.as_view(), name='contato-detail'),
    path('api/campanhas/', CampanhaListCreateView.as_view(), name='campanha-list-create'),
    # path("webhooks/", views.webhook_receiver, name='webhook_receiver'),
]
