from django.db import models


# processos/models.py


class FluxoCaptacao(models.Model):
    STATUS_CHOICES = [
        ('A fazer', 'A fazer'),
        ('Em andamento', 'Em andamento'),
        ('Concluído', 'Concluído'),
    ]

    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='A fazer')

    def __str__(self):
        return self.title
    


