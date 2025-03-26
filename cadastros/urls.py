from django.urls import path
from . import views  # Importa as views do app
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('adicionar-contato/', views.adicionar_contato, name='adicionar_contato'),
    path('visualizar-contato/', views.visualizar_contato, name='visualizar_contato'),
    path('cadastro_mensagens/', views.lista_mensagens_cadastradas, name='lista_mensagens_cadastradas'),
    path('cadastro_mensagens/nova-mensagem', views.cadastro_mensagens, name='cadastro_mensagens'),
    path('mensagens/<int:id>/', views.detalhe_mensagem_cadastrada, name='detalhe_mensagem_cadastrada'),
    path('campanhas/', views.listar_campanhas, name='listar_campanhas'),
    path('nova-campanha/', views.nova_campanha, name='nova_campanha'),
    path('enviar-email-html/', views.enviar_email_html, name='enviar_email_html'),
    path('clonar-mensagem/<int:id>/', views.clonar_mensagem, name='clonar_mensagem'),
    path('automacoes/email/', views.enviar_email_html, name='enviar_email_html'),
    path('automacoes/fluxos/', views.lista_fluxos_automacao, name='lista_fluxos_automacao'),
    path('automacoes/fluxos/novo/', views.novo_fluxo_automacao, name='novo_fluxo_automacao'),
    path('automacoes/fluxos/<int:fluxo_id>/etapas/', views.adicionar_etapas_fluxo, name='adicionar_etapas_fluxo'),
    path('automacoes/fluxos/<int:fluxo_id>/editar/', views.editar_fluxo_automacao, name='editar_fluxo_automacao'),
    path('automacoes/fluxos/<int:fluxo_id>/visualizar/', views.visualizar_fluxo_automacao, name='visualizar_fluxo_automacao'),
    path('api/cadastro-landing/', views.cadastro_landing_page, name='cadastro_landing_page'),
    path('webhook/receber-mensagem/', views.webhook_receber_mensagem, name='webhook_receber_mensagem'),
    path('whatsapp/central/', views.central_whatsapp_chat, name='central_whatsapp'),
    path('whatsapp/central/<int:contato_id>/', views.central_whatsapp_chat, name='central_whatsapp_chat'),
    path('whatsapp/central/<int:contato_id>/json/', views.mensagens_json, name='mensagens_json'),
    path('enviar-mensagem-whatsapp/<int:contato_id>/', views.enviar_mensagem_whatsapp, name='enviar_mensagem_whatsapp'),



    # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]

