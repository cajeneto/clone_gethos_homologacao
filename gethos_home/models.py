from django.db import models
<<<<<<< HEAD
from django.utils.timezone import now

class Veterinario(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15, null=True)

    def __str__(self):
        return self.nome

class Contato(models.Model):
    STATUS_CHOICES = [
        ('Agendado', 'Agendado'),
        ('Confirmado', 'Confirmado'),
        ('Cancelado', 'Cancelado'),
    ]

    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    nome_animal = models.CharField(max_length=50)
    veterinario = models.ForeignKey(Veterinario, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Agendado')
    data_consulta = models.DateField(null=True, db_index=True)  # Adicionando índice
    hora_consulta = models.TimeField(null=True)
    tipo_atendimento = models.CharField(max_length=100)
    # observacoes = models.TextField(null=True)
    empresa = models.CharField(max_length=100, null=True, blank=True)

    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.nome_animal}"

    class Meta:
        indexes = [
            models.Index(fields=["data_consulta"]),  # Indexação para melhorar performance
        ]


class Campanha(models.Model):
    nome = models.CharField(max_length=100)
    mensagem = models.TextField()  # Mensagem com variáveis como {nome}
    contatos = models.ManyToManyField('Contato', related_name='campanhas')
    criada_em = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pendente', 'Pendente'), ('Enviando', 'Enviando'), ('Concluída', 'Concluída')],
        default='Pendente'
    )

    def __str__(self):
        return self.nome

class MensagemWhatsApp(models.Model):
    campanha = models.ForeignKey(Campanha, on_delete=models.CASCADE, null=True, blank=True)  # Novo campo
    contato = models.ForeignKey(Contato, on_delete=models.CASCADE)
    mensagem = models.TextField()
    data_envio = models.DateTimeField(null=True, blank=True)
    enviado = models.BooleanField(default=False)

    def __str__(self):
        return f"Mensagem para {self.contato.nome}"

















=======

class Contato(models.Model):
    STATUS_CHOICES = [
        ('Ativo', 'Ativo'),
        ('Inativo', 'Inativo'),
    ]

    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15)
    empresa = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Ativo')
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
    
>>>>>>> backup-local

