from django.urls import path
from . import views
app_name = 'landing_page_gethos'

urlpatterns = [
    path('api/receber-dados/', views.receber_dados_landing, name='receber_dados_landing'),
]