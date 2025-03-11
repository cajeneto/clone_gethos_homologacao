import httpx
import requests
import logging
from django.core.cache import cache
from celery import shared_task
from .models import MensagemWhatsApp
from processos.models import FluxoCaptacao

logger = logging.getLogger(__name__)

EVOLUTION_API_URL = "https://gethosdev.gethostecnologia.com.br/message/sendText/gethosnotifica"
TOKEN = "zy64iz5z2x8betsuk2rp4r"
@shared_task
def enviar_mensagem_api(mensagem_id):
    logger.info(f"Iniciando envio da mensagem para o ID {mensagem_id}")

    try:
        mensagem = MensagemWhatsApp.objects.get(id=mensagem_id)
        telefone = mensagem.contato.telefone
        nomeCliente = mensagem.contato.nome
        nomeAnimal = mensagem.contato.nome_animal if mensagem.contato.nome_animal else "seu pet"
        dataConsulta = mensagem.contato.data_consulta.strftime("%d/%m/%Y") if mensagem.contato.data_consulta else "Data não informada"
        horaConsulta = mensagem.contato.hora_consulta.strftime("%H:%M") if mensagem.contato.hora_consulta else "Horário não informado"
        veterinarioAtendimento = mensagem.contato.veterinario.nome if mensagem.contato.veterinario else "Veterinário não informado"
        tipo_atendimento = mensagem.contato.tipo_atendimento
        mensagem_digitada = mensagem.mensagem  

        # Debug no terminal
        logger.info(f"Enviando mensagem para {telefone}: {mensagem_digitada}")
        
        
         # Mensagem digitada pelo usuário, com variáveis substituídas
        mensagem_digitada = mensagem.mensagem
        mensagem_final = (
            mensagem_digitada
            .replace("{{nome}}", nomeCliente)
            .replace("{{nome_animal}}", nomeAnimal)
            .replace("{{data_consulta}}", dataConsulta)
            .replace("{{hora_consulta}}", horaConsulta)
            .replace("{{tipo_atendimento}}", tipo_atendimento)
            .replace("{{veterinario}}", veterinarioAtendimento)

        )


        payload = {
            "number": telefone, 
            "text": mensagem_final,
            }

        headers = {
            "Content-Type": "application/json",
            "apikey": TOKEN
        }

        response = requests.post(EVOLUTION_API_URL, json=payload, headers=headers, timeout=10)

        if response.status_code in range(200, 300):
            mensagem.enviado = True
            mensagem.save()

            # Mover o card para "Em andamento"
            fluxo, created = FluxoCaptacao.objects.get_or_create(
                contato=mensagem.contato,
                defaults={'titulo': f"{nomeCliente} - {mensagem.contato.nome_animal}", 'status': 'A fazer'}
            )
            logger.info(f"Fluxo para {nomeCliente}: criado={created}, status atual={fluxo.status}")
            fluxo.status = 'Em andamento'
            fluxo.save()
            logger.info(f"Fluxo atualizado para 'Em andamento' para {nomeCliente}")

            logger.info(f"Mensagem enviada com sucesso para {mensagem.contato.nome}")
            return f"Mensagem enviada para {mensagem.contato.nome}"
        else:
            logger.error(f"Erro no envio para {mensagem.contato.nome}: {response.text}")
            return f"Erro no envio: {response.text}"

    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        return f"Erro inesperado ao enviar mensagem."




















# import httpx
# from django.core.cache import cache

# from celery import shared_task
# import requests
# from .models import MensagemWhatsApp



# EVOLUTION_API_URL = "https://gethosdev.gethostecnologia.com.br/message/sendText/gethosnotifica"
# TOKEN = "zy64iz5z2x8betsuk2rp4r"

# @shared_task
# def enviar_mensagem_api(mensagem_id):
#     mensagem = MensagemWhatsApp.objects.get(id=mensagem_id)

#     # Captura os dados do contato para personalizar a mensagem
#     telefone = mensagem.contato.telefone
#     nomeCliente = mensagem.contato.nome
#     nomeAnimal = mensagem.contato.nome_animal
#     dataConsulta = mensagem.contato.data_consulta.strftime("%d/%m/%Y") if mensagem.contato.data_consulta else "Data não informada"
#     horaConsulta = mensagem.contato.hora_consulta.strftime("%H:%M") if mensagem.contato.hora_consulta else "Horário não informado"
#     veterinarioAtendimento = mensagem.contato.veterinario.nome if mensagem.contato.veterinario else "Veterinário não informado"
#     tipoatendimento = mensagem.contato.tipo_atendimento




#      # Texto digitado pelo usuário no textarea
#     mensagem_digitada = mensagem.mensagem  # Isso já vem do formulário
    
    
    
    
#     # Payload ajustado
#     payload = {
#         "number": telefone, 
#         "textMessage": {
#             "text": f"""Olá, *{nomeCliente}*! 🐾
# Seja bem-vindo(a) a *Gethos Veterinária*!

# Ficamos felizes em tê-lo(a) por aqui. 😊

# Só para lembrar que o atendimento do seu pet *{nomeAnimal}* está agendado no dia: 

# 📅 Data: *{dataConsulta}*
# ⏰ Horário: *{horaConsulta}*
# 🩺 Veterinário: *Dr. {veterinarioAtendimento}*
# 🏥 Atendimento: *{tipoatendimento}*

# 📩 Mensagem personalizada: *{mensagem_digitada}*

# Estamos ansiosos para recebê-los e garantir o melhor cuidado. 🐾💙

# *Digite uma das opções abaixo: 😁👇*

# *1* - Sim, confirmo
# *2* - Não, desejo reagendar
# *3* - Tenho dúvidas

# _Esta é uma mensagem automática_"""
#         },
#         "delay": 1000,
#         "quoted": {
#             "key": {
#                 "remoteJid": "string",
#                 "fromMe": True,
#                 "id": "string"
#             },
#             "message": {"conversation": "string"}
#         },
#         "linkPreview": True,
#         "mentionsEveryOne": True,
#         "mentioned": ["string"]
#     }





#     headers = {
#         "Content-Type": "application/json",
#         "apikey": TOKEN
#         }

#     response = requests.post(EVOLUTION_API_URL, json=payload, headers=headers)

#     if response.status_code == 201:
#         mensagem.enviado = True
#         mensagem.save()
#         return f"Mensagem enviada para {mensagem.contato.nome}"
#     else:
#         return f"Erro ao enviar mensagem: {response.text}"




















# EVOLUTION_API_URL = "https://api.evolution.com"
# TOKEN = "seu_token_aqui"

# # Função assíncrona para obter dados da API
# async def obter_dados_api():
#     headers = {"Authorization": f"Bearer {TOKEN}"}
#     async with httpx.AsyncClient() as client:
#         response = await client.get(f"{EVOLUTION_API_URL}/dados", headers=headers)
#         return response.json() if response.status_code == 200 else None

# # Função assíncrona para buscar no cache ou chamar a API
# async def obter_dados_cache():
#     dados = cache.get("dados_api")
#     if not dados:
#         dados = await obter_dados_api()  # Agora chamamos corretamente com await
#         cache.set("dados_api", dados, timeout=3600)  # Expira em 1 hora
#     return dados



# import requests
# import threading

# EVOLUTION_API_URL = "https://api.evolution.com"
# TOKEN = "seu_token_aqui"

# def obter_dados_api():
#     """Executa a requisição da API em uma thread separada."""
#     headers = {"Authorization": f"Bearer {TOKEN}"}
#     resultado = {}

#     def request_thread():
#         nonlocal resultado
#         response = requests.get(f"{EVOLUTION_API_URL}/dados", headers=headers)
#         if response.status_code == 200:
#             resultado = response.json()

#     thread = threading.Thread(target=request_thread)
#     thread.start()
#     thread.join()  # Aguarda a thread finalizar

#     return resultado



