from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Contato  # Inclua outros modelos, se já existirem

admin.site.register(Usuario, UserAdmin)

