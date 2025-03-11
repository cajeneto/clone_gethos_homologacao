from celery import shared_task
from django.utils import timezone
from gethos_home.models import Campanha, MensagemWhatsApp
from gethos_home.api import enviar_mensagem_api
import time

@shared_task
def enviar_campanha(campanha_id, intervalo=10):
    campanha = Campanha.objects.get(id=campanha_id)
    campanha.status = 'Enviando'
    campanha.save()

    for i, contato in enumerate(campanha.contatos.all()):
        if i > 0:  # Espera antes de enviar, exceto na primeira mensagem
            time.sleep(intervalo)
        
        # Criar a mensagem
        mensagem = MensagemWhatsApp.objects.create(
            campanha=campanha,
            contato=contato,
            mensagem=campanha.mensagem,
            data_envio=timezone.now()
        )
        # Enviar a mensagem
        enviar_mensagem_api(mensagem.id)

    campanha.status = 'Concluída'
    campanha.save()