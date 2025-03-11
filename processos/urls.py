from django.urls import path
from . import views




urlpatterns = [
    path('enviarMensagens/', views.fluxo_captacao, name='fluxo_captacao'),
    path('add_etapa/', views.add_etapa, name='add_etapa'),
    path('edit_etapa/<int:ip_etapa>/', views.edit_etapa, name='edit_etapa'),
    path('delete_etapa/<int:ip_etapa>/', views.delete_etapa, name='delete_etapa'),
    path('enviar_mensagem/', views.enviar_mensagem, name='enviar_mensagem' )
    # path('move-task/', views.move_task, name='move_task'),
]
