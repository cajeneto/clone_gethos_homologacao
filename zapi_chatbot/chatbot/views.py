from django.shortcuts import render


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import requests

# Configurações da Z-API
Z_API_INSTANCE = "3D647FFC69B400D738AF3E0DE9D9E9B8"
Z_API_TOKEN = "1AEDCE4DDED8615D8D50B80E"
Z_API_CLIENT_TOKEN = "F1134eeca2cf748be89c29ca317faf019S"

@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Extrair informações da mensagem recebida
        if 'text' in data and 'message' in data['text']:
            message = data['text']['message']
            sender = data['phone']
            
            # Processar a mensagem
            response = process_message(message)
            
            # Enviar resposta
            send_response(sender, response)
            
            return JsonResponse({"status": "success"}, status=200)
        else:
            return JsonResponse({"status": "error", "message": "Invalid message format"}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

def process_message(message):
    message = message.lower()
    if "olá" in message or "oi" in message:
        return "Olá! Como posso ajudar?"
    elif "preço" in message:
        return "Nossos preços começam a partir de R$ 99,90."
    else:
        return "Desculpe, não entendi. Pode reformular?"

def send_response(phone, message):
    url = f"https://api.z-api.io/instances/{Z_API_INSTANCE}/token/{Z_API_TOKEN}/send-text"
    
    payload = {
        "phone": phone,
        "message": message
    }
    
    headers = {
        "Content-Type": "application/json",
        "Client-Token": Z_API_CLIENT_TOKEN
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        print("Mensagem enviada com sucesso!")
    else:
        print("Erro ao enviar mensagem:", response.text)
