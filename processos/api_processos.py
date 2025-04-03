import requests
import logging
from celery import shared_task
from gethos_home.models import Contato  # Assume que Contato está em processos/models.py
from cadastros.models import ModeloMensagem
from django.core.mail import EmailMultiAlternatives
from configuracoes.models import APIEvoGetInstance, EmailSMTPUsuario

logger = logging.getLogger(__name__)

@shared_task
def enviar_mensagem_api(contato_id, modelo_id, canal):
    """
    Envio de mensagem usando um modelo salvo no banco de dados.
    Pode ser chamado de forma assíncrona com .delay() do Celery.
    Usa a primeira instância de APIEvoGetInstance disponível.
    """
    contato = Contato.objects.get(id=contato_id)
    modelo = ModeloMensagem.objects.get(id=modelo_id)
    
    texto = modelo.conteudo_mensagem.replace("@nome", contato.nome)

    # Pega a primeira instância de APIEvoGetInstance
    instancia = APIEvoGetInstance.objects.first()
    smtp_config = EmailSMTPUsuario.objects.first()

    if not instancia:
        logger.error("❌ Nenhuma instância encontrada em APIEvoGetInstance")
        return False

    EVOLUTION_API_URL = f"https://gethosdev.gethostecnologia.com.br/message/sendText/{instancia.instance_name}"

    if canal == 'whatsapp':
        payload = {
            "number": contato.telefone,
            "text": texto
        }
        headers = {
            'Content-Type': 'application/json',
            'apikey': instancia.api_key,
        }
        response = requests.post(EVOLUTION_API_URL, json=payload, headers=headers)
        if response.status_code == 200:
            logger.info(f"✅ WhatsApp enviado com sucesso para {contato.nome}")
            return True
        else:
            logger.error(f"❌ Falha ao enviar WhatsApp: {response.text}")
            return False
    
    elif canal == 'email' and smtp_config:
        email = EmailMultiAlternatives(
            subject="Mensagem do Gethos CRM",
            body=texto,
            from_email=smtp_config.remetente_email_usuario,
            to=[contato.email]
        )
        email.attach_alternative(texto, "text/html")
        email.send()
        logger.info(f"✅ E-mail enviado com sucesso para {contato.email}")
        return True
    
    return False

@shared_task
def enviar_mensagem_texto(contato_id, texto, canal):
    """
    Envio de mensagem usando texto livre.
    Pode ser chamado de forma assíncrona com .delay() do Celery.
    Usa a primeira instância de APIEvoGetInstance disponível.
    """
    contato = Contato.objects.get(id=contato_id)
    texto = texto.replace("@nome", contato.nome)

    # Pega a primeira instância de APIEvoGetInstance
    instancia = APIEvoGetInstance.objects.first()
    smtp_config = EmailSMTPUsuario.objects.first()

    if not instancia:
        logger.error("❌ Nenhuma instância encontrada em APIEvoGetInstance")
        return False

    EVOLUTION_API_URL = f"https://gethosdev.gethostecnologia.com.br/message/sendText/{instancia.instance_name}"

    if canal == 'whatsapp':
        payload = {
            "number": contato.telefone,
            "text": texto
        }
        headers = {
            'Content-Type': 'application/json',
            'apikey': instancia.api_key,
        }
        response = requests.post(EVOLUTION_API_URL, json=payload, headers=headers)
        if response.status_code == 200:
            logger.info(f"✅ WhatsApp enviado com sucesso para {contato.nome}")
            return True
        else:
            logger.error(f"❌ Falha ao enviar WhatsApp: {response.text}")
            return False

    elif canal == 'email' and smtp_config:
        email = EmailMultiAlternatives(
            subject="Mensagem do Gethos CRM",
            body=texto,
            from_email=smtp_config.remetente_email_usuario,
            to=[contato.email]
        )
        email.attach_alternative(texto, "text/html")
        email.send()
        logger.info(f"✅ E-mail enviado com sucesso para {contato.email}")
        return True
    
    return False