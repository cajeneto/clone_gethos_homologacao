from django.contrib import admin
from .models import FluxoAutomatizado, EtapaFluxo, ExecucaoFluxo

# Register your models here.
admin.site.register(FluxoAutomatizado)
admin.site.register(EtapaFluxo)
admin.site.register(ExecucaoFluxo)