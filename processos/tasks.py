from celery import shared_task
from django.utils import timezone
from gethos_home.models import Campanha, MensagemWhatsApp
from processos.api_processos import enviar_mensagem_texto  # Importa a função ajustada
import time
import logging

logger = logging.getLogger(__name__)

@shared_task
def enviar_campanha(campanha_id, intervalo=10):
    try:
        logger.info(f"Iniciando tarefa para campanha ID: {campanha_id}")
        campanha = Campanha.objects.get(id=campanha_id)
        campanha.status = 'Enviando'
        campanha.save()
        logger.info(f"Status da campanha {campanha_id} alterado para 'Enviando'")

        for i, contato in enumerate(campanha.contatos.all()):
            if i > 0:
                time.sleep(intervalo)
            
            mensagem = MensagemWhatsApp.objects.create(
                campanha=campanha,
                contato=contato,
                mensagem=campanha.mensagem,
                data_envio=timezone.now()
            )
            logger.info(f"Mensagem criada para contato {contato.id}")

            # Usa a nova função sem user_id
            sucesso = enviar_mensagem_texto(
                contato.id,
                campanha.mensagem,
                canal='whatsapp'
            )
            if sucesso:
                logger.info(f"Mensagem enviada com sucesso para contato {contato.id}")
            else:
                logger.error(f"Falha ao enviar mensagem para contato {contato.id}")

        campanha.status = 'Concluída'
        campanha.save()
        logger.info(f"Campanha {campanha_id} concluída com sucesso")
    except Campanha.DoesNotExist:
        logger.error(f"Campanha com ID {campanha_id} não encontrada")
        raise
    except Exception as e:
        logger.error(f"Erro ao processar campanha {campanha_id}: {str(e)}")
        if 'campanha' in locals():
            campanha.status = 'Erro'
            campanha.save()
        raise