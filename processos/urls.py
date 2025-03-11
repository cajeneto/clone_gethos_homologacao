from django.urls import path
from . import views

<<<<<<< HEAD



urlpatterns = [
    path('enviarMensagens/', views.fluxo_captacao, name='fluxo_captacao'),
    path('add_etapa/', views.add_etapa, name='add_etapa'),
    path('edit_etapa/<int:ip_etapa>/', views.edit_etapa, name='edit_etapa'),
    path('delete_etapa/<int:ip_etapa>/', views.delete_etapa, name='delete_etapa'),
    path('enviar_mensagem/', views.enviar_mensagem, name='enviar_mensagem' )
    # path('move-task/', views.move_task, name='move_task'),
]
=======
urlpatterns = [
    path('', views.fluxo_captacao, name='fluxo_captacao'),  # Alterei para raiz do módulo
    path('add_etapa/', views.add_etapa, name='add_etapa'),
    path('edit_etapa/<int:id_etapa>/', views.edit_etapa, name='edit_etapa'),
    path('delete_etapa/<int:id_etapa>/', views.delete_etapa, name='delete_etapa'),
    path('enviar_mensagem/', views.enviar_mensagem, name='enviar_mensagem'),
    path('move-task/', views.move_task, name='move_task'),  # Novo endpoint
    path('relatorios/', views.relatorios, name='relatorios'), #PENDENTE DE TESTES!
]









# from django.urls import path
# from . import views




# urlpatterns = [
#     path('enviarMensagens/', views.fluxo_captacao, name='fluxo_captacao'),
#     path('add_etapa/', views.add_etapa, name='add_etapa'),
#     path('edit_etapa/<int:ip_etapa>/', views.edit_etapa, name='edit_etapa'),
#     path('delete_etapa/<int:ip_etapa>/', views.delete_etapa, name='delete_etapa'),
#     path('enviar_mensagem/', views.enviar_mensagem, name='enviar_mensagem' )
#     # path('move-task/', views.move_task, name='move_task'),
# ]
>>>>>>> 829be17 (Versão CRM GETHOS 1.3 - COM REST API)
