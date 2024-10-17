from django.db import models

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

    def __str__(self):
        return self.nome
    

