# Em processos/tasks.py

from celery import shared_task
from django.utils import timezone
from gethos_home.models import Campanha, MensagemWhatsApp
from gethos_home.api import enviar_mensagem_api, enviar_mensagem_api_livre
import time

@shared_task
def enviar_campanha(campanha_id, intervalo=10):
    campanha = Campanha.objects.get(id=campanha_id)
    campanha.status = 'Enviando'
    campanha.save()

    for i, contato in enumerate(campanha.contatos.all()):
        if i > 0:
            time.sleep(intervalo)
        
        mensagem = MensagemWhatsApp.objects.create(
            campanha=campanha,
            contato=contato,
            mensagem=campanha.mensagem,
            data_envio=timezone.now()
        )

        # esse parametro é para utilizar somente em processos/enviar whatsapp
        enviar_mensagem_api_livre(contato.id, campanha.mensagem, canal='whatsapp')

    campanha.status = 'Concluída'
    campanha.save()