# import_contatos.py
import json
import requests

API_URL = "http://127.0.0.1:8000/api/contatos/"
HEADERS = {"Content-Type": "application/json"}

# Carregar os contatos do arquivo JSON
with open('contatos.json', 'r', encoding='utf-8') as file:
    contatos = json.load(file)

# Enviar cada contato
for contato in contatos:
    response = requests.post(API_URL, headers=HEADERS, json=contato)
    if response.status_code == 201:
        print(f"Contato {contato['nome']} criado com sucesso!")
    else:
        print(f"Erro ao criar {contato['nome']}: {response.text}")