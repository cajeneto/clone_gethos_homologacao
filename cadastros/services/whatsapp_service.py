# cadastros/services/whatsapp_service.py

import requests
from django.conf import settings
from gethos_home.api import TOKEN

def enviar_mensagem_evolution_service(telefone, mensagem):
    url = "https://gethosdev.gethostecnologia.com.br/message/sendText/gethosnotifica"
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
