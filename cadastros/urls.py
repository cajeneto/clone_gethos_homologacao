from django.urls import path
from . import views  # Importa as views do app

urlpatterns = [
    path('adicionar-contato/', views.adicionar_contato, name='adicionar_contato'),
    path('visualizar-contato/', views.visualizar_contato, name='visualizar_contato'),
]