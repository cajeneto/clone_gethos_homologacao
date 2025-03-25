from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    # path('accounts/', include('django.contrib.auth.urls')),  # URLs de login/logout
    path("", include("gethos_home.urls")), 
    path('cadastros/', include('cadastros.urls')),  # Inclui as URLs do app 'cadastros'
    path('processos/', include('processos.urls')),  # Inclui as URLs do app 'processos' 
    # path('api/', include('gethos_home.urls')),  
            
    ]
