import requests
import logging
from celery import shared_task
from .models import Contato, Usuario
from cadastros.models import ModeloMensagem
from django.core.mail import EmailMultiAlternatives
from configuracoes.models import APIEvoGetInstance, EmailSMTPUsuario


logger = logging.getLogger(__name__)

@shared_task
def enviar_mensagem_api(contato_id, modelo_id, canal, user_id=None):
    """
    Envio de mensagem usando um modelo salvo no banco de dados.
    Pode ser chamado de forma assíncrona com .delay() do Celery
    """
    from django.contrib.auth.models import User
    contato = Contato.objects.get(id=contato_id)
    modelo = ModeloMensagem.objects.get(id=modelo_id)
    
    # User pode ser opcional
    user = User.objects.get(id=user_id) if user_id else None
    
    texto = modelo.conteudo_mensagem.replace("@nome", contato.nome)

    # Procura instância pela chave user se fornecido, ou pega a primeira
    if user:
        instancia = APIEvoGetInstance.objects.filter(user=user).first()
        smtp_config = EmailSMTPUsuario.objects.filter(user=user).first()
    else:
        instancia = APIEvoGetInstance.objects.first()
        smtp_config = EmailSMTPUsuario.objects.first()

    if not instancia:
        logger.error(f"❌ Nenhuma instância encontrada")
        return

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
def enviar_mensagem_texto(contato_id, texto, canal, user_id=None):
    """
    Envio de mensagem usando texto livre.
    Pode ser chamado de forma assíncrona com .delay() do Celery
    
    Esta função substitui 'enviar_mensagem_api_livre'
    """
    contato = Contato.objects.get(id=contato_id)
    texto = texto.replace("@nome", contato.nome)

    # Procura instância pela chave user se fornecido, ou pega a primeira
    if user_id:
        from django.contrib.auth.models import User
        user = Usuario.objects.get(id=user_id)
        instancia = APIEvoGetInstance.objects.filter(user=user).first()
        smtp_config = EmailSMTPUsuario.objects.filter(user=user).first()
    else:
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
























# import requests
# import logging
# from celery import shared_task
# from .models import Contato
# from cadastros.models import ModeloMensagem
# from django.core.mail import EmailMultiAlternatives
# from configuracoes.models import APIEvoGetInstance, EmailSMTPUsuario

# logger = logging.getLogger(__name__)




# @shared_task
# def enviar_mensagem_api(contato_id, modelo_id, canal, user_id):
#     from django.contrib.auth.models import User
#     contato = Contato.objects.get(id=contato_id)
#     modelo = ModeloMensagem.objects.get(id=modelo_id)
#     user = User.objects.get(id=user_id)
    
#     texto = modelo.conteudo_mensagem.replace("@nome", contato.nome)

#     instancia = APIEvoGetInstance.objects.filter(user=user).first()
#     smtp_config = EmailSMTPUsuario.objects.filter(user=user).first()

#     if not instancia:
#         logger.error(f"❌ Nenhuma instância encontrada para o usuário {user.username}")
#         return

#     EVOLUTION_API_URL = f"https://gethosdev.gethostecnologia.com.br/message/sendText/{instancia.instance_name}"

#     if canal == 'whatsapp':
#         payload = {
#             "number": contato.telefone,
#             "text": texto
#         }
#         headers = {
#             'Content-Type': 'application/json',
#             'apikey': instancia.api_key,
#         }
#         response = requests.post(EVOLUTION_API_URL, json=payload, headers=headers)
#         if response.status_code == 200:
#             logger.info(f"✅ WhatsApp enviado com sucesso para {contato.nome}")
#         else:
#             logger.error(f"❌ Falha ao enviar WhatsApp: {response.text}")

    

    
#     elif canal == 'email' and smtp_config:
#         email = EmailMultiAlternatives(
#             subject="Mensagem do Gethos CRM",
#             body=texto,
#             from_email=smtp_config.remetente_email_usuario,
#             to=[contato.email]
#         )
#         email.attach_alternative(texto, "text/html")
#         email.send()
#         logger.info(f"✅ E-mail enviado com sucesso para {contato.email}")




# def enviar_mensagem_api_livre(contato_id, texto, canal, user_id):
#     from django.contrib.auth.models import User
#     contato = Contato.objects.get(id=contato_id)
#     user = User.objects.get(id=user_id)
#     texto = texto.replace("@nome", contato.nome)

#     instancia = APIEvoGetInstance.objects.filter(user=user).first()
#     smtp_config = EmailSMTPUsuario.objects.filter(user=user).first()


#     if not instancia:
#         logger.error(f"❌ Nenhuma instância encontrada para o usuário {user.username}")
#         return

#     EVOLUTION_API_URL = f"https://gethosdev.gethostecnologia.com.br/message/sendText/{instancia.instance_name}"



#     if canal == 'whatsapp':
#         payload = {
#             "number": contato.telefone,
#             "text": texto
#         }
#         headers = {
#             'Content-Type': 'application/json',
#             'apikey': instancia.api_key,
#         }
#         response = requests.post(EVOLUTION_API_URL, json=payload, headers=headers)
#         if response.status_code == 200:
#             logger.info(f"✅ WhatsApp enviado com sucesso para {contato.nome}")
#         else:
#             logger.error(f"❌ Falha ao enviar WhatsApp: {response.text}")


#     elif canal == 'email' and smtp_config:
#         email = EmailMultiAlternatives(
#             subject="Mensagem do Gethos CRM",
#             body=texto,
#             from_email=smtp_config.remetente_email_usuario,
#             to=[contato.email]
#         )
#         email.attach_alternative(texto, "text/html")
#         email.send()
#         logger.info(f"✅ E-mail enviado com sucesso para {contato.email}")








# import requests
# import logging
# from django.core.cache import cache
# from celery import shared_task
# from .models import MensagemWhatsApp, Contato
# from processos.models import FluxoCaptacao
# from cadastros.models import ModeloMensagem
# from django.core.mail import EmailMultiAlternatives

# logger = logging.getLogger(__name__)

# EVOLUTION_API_URL = "https://gethosdev.gethostecnologia.com.br/message/sendText/gethosnotifica"
# TOKEN = "zy64iz5z2x8betsuk2rp4r"


# @shared_task
# def enviar_mensagem_api(contato_id, mensagem_id, canal):
#     logger.info(f"Iniciando envio da mensagem para o ID {mensagem_id}")
#     contato = Contato.objects.get(id=contato_id)
#     mensagem = ModeloMensagem.objects.get(id=mensagem_id)

#     if canal == 'whatsapp':
#         # Exemplo com Evolution API (WhatsApp)
#         url = EVOLUTION_API_URL
#         payload = {
#             "number": contato.telefone,
#             "message": mensagem.conteudo_mensagem.replace("@nome", contato.nome)
#         }
#         headers = {
#             'Authorization': TOKEN
#         }
#         response = requests.post(url, json=payload, headers=headers)
#         if response.status_code == 200:
#             print(f"✅ WhatsApp enviado com sucesso para {contato.nome}")
#         else:
#             print(f"❌ Falha ao enviar WhatsApp: {response.text}")

#     elif canal == 'email':
#         email_msg = EmailMultiAlternatives(
#             subject="Mensagem do Gethos CRM",
#             body="Versão alternativa para leitores antigos.",
#             from_email="seuemail@dominio.com",
#             to=[contato.email]
#         )
#         email_msg.attach_alternative(mensagem.conteudo_mensagem.replace("@nome", contato.nome), "text/html")
#         email_msg.send()
#         print(f"✅ E-mail enviado com sucesso para {contato.email}")

#     try:
#         mensagem = MensagemWhatsApp.objects.get(id=mensagem_id)
#         telefone = mensagem.contato.telefone
#         nomeCliente = mensagem.contato.nome
#         mensagem_digitada = mensagem.mensagem  

#         # Debug no terminal
#         logger.info(f"Enviando mensagem para {telefone}: {mensagem_digitada}")
        
        
#          # Mensagem digitada pelo usuário, com variáveis substituídas
#         mensagem_digitada = mensagem.mensagem
#         mensagem_final = (
#             mensagem_digitada
#             .replace("@nome", nomeCliente)
            
#         )


#         payload = {
#             "number": telefone, 
#             "text": mensagem_final,
#             }

#         headers = {
#             "Content-Type": "application/json",
#             "apikey": TOKEN
#         }

#         response = requests.post(EVOLUTION_API_URL, json=payload, headers=headers, timeout=10)

#         if response.status_code in range(200, 300):
#             mensagem.enviado = True
#             mensagem.save()

#             # Mover o card para "Em andamento"
#             fluxo, created = FluxoCaptacao.objects.get_or_create(
#                 contato=mensagem.contato,
#                 defaults={'titulo': f"{nomeCliente} - {mensagem.contato.nome_animal}", 'status': 'A fazer'}
#             )
#             logger.info(f"Fluxo para {nomeCliente}: criado={created}, status atual={fluxo.status}")
#             fluxo.status = 'Em andamento'
#             fluxo.save()
#             logger.info(f"Fluxo atualizado para 'Em andamento' para {nomeCliente}")

#             logger.info(f"Mensagem enviada com sucesso para {mensagem.contato.nome}")
#             return f"Mensagem enviada para {mensagem.contato.nome}"
#         else:
#             logger.error(f"Erro no envio para {mensagem.contato.nome}: {response.text}")
#             return f"Erro no envio: {response.text}"

#     except Exception as e:
#         logger.error(f"Erro inesperado: {str(e)}")
#         return f"Erro inesperado ao enviar mensagem."









