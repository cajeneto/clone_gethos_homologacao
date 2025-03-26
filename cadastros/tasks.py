# cadastros/tasks.py
from celery import shared_task
from .models import ExecucaoFluxo, EtapaFluxo
from gethos_home.api import enviar_mensagem_api
from datetime import timedelta
from django.utils import timezone

@shared_task
def iniciar_execucao_fluxo(execucao_fluxo_id):
    try:
        execucao = ExecucaoFluxo.objects.get(id=execucao_fluxo_id)
        etapas = EtapaFluxo.objects.filter(fluxo=execucao.fluxo).order_by('ordem')

        tempo_total = timedelta()

        for etapa in etapas:
            if etapa.intervalo_tipo == 'minutos':
                tempo_total += timedelta(minutes=etapa.delay_intervalo)
            else:
                tempo_total += timedelta(hours=etapa.delay_intervalo)

            enviar_mensagem_api.apply_async(
                args=[execucao.contato.id, etapa.mensagem.id, etapa.canal],
                eta=timezone.now() + tempo_total
            )
        print(f"✅ Fluxo {execucao.fluxo.nome} agendado com sucesso!")
    except ExecucaoFluxo.DoesNotExist:
        print("❌ ExecucaoFluxo não encontrada!")
