from django.db import models
from gethos_home.models import Contato

class FluxoCaptacao(models.Model):
    STATUS_CHOICES = [
        ('A fazer', 'A fazer'),
        ('Em andamento', 'Em andamento'),
        ('Concluído', 'Concluído'),
    ]

    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='A fazer')
    contato = models.ForeignKey(Contato, on_delete=models.CASCADE, null=True, blank=True)  # Associação com Contato
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['created_at']
        
