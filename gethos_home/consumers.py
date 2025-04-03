import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from gethos_home.models import Contato
from cadastros.models import MensagemWhatsApp
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.contato_id = self.scope['url_route']['kwargs']['contato_id']
        self.room_name = f'chat_{self.contato_id}'
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        remetente = data.get('remetente', 'CRM')

        # Salva no banco de dados
        await self.salvar_mensagem(remetente, self.contato_id, message)

        # Reenvia para o grupo
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'remetente': remetente,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'remetente': event['remetente']
        }))

    @database_sync_to_async
    def salvar_mensagem(self, remetente, contato_id, message):
        contato = Contato.objects.get(id=contato_id)
        MensagemWhatsApp.objects.create(
            contato=contato,
            mensagem=message,
            tipo='enviada' if remetente == 'CRM' else 'recebida',
            enviado=True,
            data_envio=timezone.now()
        )
