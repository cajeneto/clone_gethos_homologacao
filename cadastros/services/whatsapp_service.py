# cadastros/services/whatsapp_service.py

import requests
from django.conf import settings
from configuracoes.models import APIEvoGetInstance

TOKEN = APIEvoGetInstance.objects.first().api_key
INSTANCIA = APIEvoGetInstance.objects.first().instance_name

def enviar_mensagem_evolution_service(telefone, mensagem):
    url = f"https://gethosdev.gethostecnologia.com.br/message/sendText/{INSTANCIA}"
    headers = {
        "Apikey": TOKEN,
        "Content-Type": "application/json"
    }
    payload = {
        "number": telefone,
        "text": mensagem
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"❌ Erro ao enviar mensagem: {e}")
        return False
