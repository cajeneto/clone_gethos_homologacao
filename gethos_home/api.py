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
            .replace("@nome", nomeCliente)
            .replace("@nome_animal", nomeAnimal)
            .replace("@data_consulta", dataConsulta)
            .replace("@hora_consulta", horaConsulta)
            .replace("@tipo_atendimento", tipo_atendimento)
            .replace("@veterinario", veterinarioAtendimento)

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









