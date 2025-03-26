from django.db import models
from django.utils import timezone
from gethos_home.models import Contato

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




class Campanha(models.Model):
    nome = models.CharField(max_length=255)
    # descricao = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('ativa', 'Campanha Ativa'),
        ('inativa', 'Campanha Inativa')
    ], default='ativa')

    responsavel = models.CharField(max_length=255)
    titulo = models.CharField(max_length=255)
    data_envio = models.DateField()
    hora_envio = models.TimeField()

    mensagem = models.ForeignKey(ModeloMensagem, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome




class FluxoAutomatizado(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class EtapaFluxo(models.Model):
    INTERVALO_CHOICES = [
    ('minutos', 'Minutos'),
    ('horas', 'Horas')
    ]


    fluxo = models.ForeignKey(FluxoAutomatizado, on_delete=models.CASCADE, related_name='etapas')
    ordem = models.PositiveIntegerField()
    mensagem = models.ForeignKey(ModeloMensagem, on_delete=models.CASCADE)
    canal = models.CharField(choices=[('email', 'E-mail'), ('whatsapp', 'WhatsApp')], max_length=10)
    delay_intervalo = models.PositiveIntegerField(default=0)
    intervalo_tipo = models.CharField(max_length=10, choices=INTERVALO_CHOICES, default='horas')

    def __str__(self):
        return f"{self.fluxo.nome} - Etapa {self.ordem}"


class ExecucaoFluxo(models.Model):
    contato = models.ForeignKey(Contato, on_delete=models.CASCADE)
    fluxo = models.ForeignKey(FluxoAutomatizado, on_delete=models.CASCADE)
    iniciado_em = models.DateTimeField(auto_now_add=True)
    finalizado = models.BooleanField(default=False)





class MensagemWhatsApp(models.Model):
    contato = models.ForeignKey(Contato, on_delete=models.CASCADE, related_name="mensagens_whatsapp_cadastros")
    mensagem = models.TextField()
    enviado = models.BooleanField(default=False)
    tipo = models.CharField(max_length=10, choices=[('enviada', 'Enviada'), ('recebida', 'Recebida')])
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo.upper()} - {self.contato.nome}"