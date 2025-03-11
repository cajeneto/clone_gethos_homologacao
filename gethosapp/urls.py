from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("gethos_home.urls")), 
    path('cadastros/', include('cadastros.urls')),  # Inclui as URLs do app 'cadastros'
<<<<<<< HEAD
    path('processos/', include('processos.urls')),  # Inclui as URLs do app 'processos' 
    # path('api/', include('gethos_home.urls')),  
            
=======
    path('processos/', include('processos.urls')),  # Inclui as URLs do app 'processos'            
>>>>>>> backup-local
    ]
