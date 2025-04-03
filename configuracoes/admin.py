from django.contrib import admin

from django.contrib import admin
from .models import CadastroEmpresa, EmailSMTPUsuario, APIEvoUsuario

admin.site.register(CadastroEmpresa)
admin.site.register(EmailSMTPUsuario)
admin.site.register(APIEvoUsuario)
# admin.site.register(APIEvoGetInstance)

