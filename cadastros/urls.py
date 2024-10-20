from django.urls import path

from . import views  # Importa as views do app

urlpatterns = [
    path('adicionar-contato/', views.adicionar_contato, name='adicionar_contato'),
    path('visualizar-contato/', views.visualizar_contato, name='visualizar_contato'),
    path('cadastro_mensagens/', views.lista_mensagens_cadastradas, name='lista_mensagens_cadastradas'),
    path('cadastro_mensagens/nova-mensagem', views.cadastro_mensagens, name='cadastro_mensagens'),
    path('mensagens/<int:id>/', views.detalhe_mensagem_cadastrada, name='detalhe_mensagem_cadastrada'),
]

