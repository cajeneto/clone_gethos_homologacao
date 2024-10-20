from django.db import models
from django.utils import timezone

class ModeloMensagem(models.Model):
    TIPO_MENSAGEM_CHOICES = [
        (1, 'SMS'),
        (2, 'WhatsApp'),
        (3, 'E-mail'),
    ]

    nome_modelo = models.CharField(max_length=255)
    tipo_mensagem = models.IntegerField(choices=TIPO_MENSAGEM_CHOICES)
    conteudo_mensagem = models.TextField()
    # data_criacao = models.DateTimeField(default=timezone.now)
    data_criacao = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.nome_modelo
