from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class Usuario(AbstractUser):
    whatsapp_validator = RegexValidator(
        r'^\+55\d{10,11}$',
        'Digite o número de WhatsApp no formato +5582987654321 (com código do país +55 e 10 ou 11 dígitos).'
    )
    whatsapp = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[whatsapp_validator],
        help_text="Número de WhatsApp no formato +5582987654321"
    )
    email = models.EmailField(unique=True, blank=False, null=False)

    def __str__(self):
        return self.username




class Contato(models.Model):
    STATUS_CHOICES = [
        ('Lead', 'Lead'),
        ('Cliente Ativo', 'Cliente Ativo'),
        ('Inativo', 'Inativo'),
    ]

    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100, unique=True)
    empresa = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Lead')
    observacoes = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} - {self.telefone} - {self.email}"

    @property
    def telefone_formatado(self):
        telefone = self.telefone
        if telefone.startswith('55') and len(telefone) >= 12:
            telefone = telefone[2:]  # Remove o código do país
        if len(telefone) == 11:
            return f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"
        elif len(telefone) == 10:
            return f"({telefone[:2]}) {telefone[2:6]}-{telefone[6:]}"
        return telefone





class Campanha(models.Model):
    TIPO_CHOICES = [
        ('WhatsApp', 'WhatsApp'),
        ('Email', 'E-mail'),
        ('Ambos', 'Ambos'),
    ]

    nome = models.CharField(max_length=100)
    mensagem = models.TextField()  # Mensagem com variáveis como {nome}
    contatos = models.ManyToManyField('Contato', related_name='campanhas')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='WhatsApp')  # Novo campo
    criada_em = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pendente', 'Pendente'), ('Enviando', 'Enviando'), ('Concluída', 'Concluída')],
        default='Pendente'
    )

    def __str__(self):
        return self.nome

class MensagemWhatsApp(models.Model):
    TIPO_CHOICES = [
        ('WhatsApp', 'WhatsApp'),
        ('Email', 'E-mail'),
    ]

    campanha = models.ForeignKey(Campanha, on_delete=models.CASCADE, null=True, blank=True)
    contato = models.ForeignKey(Contato, on_delete=models.CASCADE, related_name="mensagem_whatsapp_gethos_home")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='WhatsApp')  # Novo campo
    mensagem = models.TextField()
    data_envio = models.DateTimeField(null=True, blank=True)
    enviado = models.BooleanField(default=False)

    def __str__(self):
        return f"Mensagem ({self.tipo}) para {self.contato.nome}"
















