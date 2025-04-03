from django.urls import path
from . import views

urlpatterns = [
    path('', views.configuracoes_view, name='configuracoes'),
    path('atualizar_whatsapp/', views.atualizar_whatsapp_view, name='atualizar_whatsapp'),
]