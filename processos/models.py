from django.db import models
<<<<<<< HEAD


# processos/models.py

=======
from gethos_home.models import Contato
>>>>>>> 829be17 (Versão CRM GETHOS 1.3 - COM REST API)

class FluxoCaptacao(models.Model):
    STATUS_CHOICES = [
        ('A fazer', 'A fazer'),
        ('Em andamento', 'Em andamento'),
        ('Concluído', 'Concluído'),
    ]

    titulo = models.CharField(max_length=100)
<<<<<<< HEAD
    descricao = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='A fazer')

    def __str__(self):
        return self.title
    


=======
    descricao = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='A fazer')
    contato = models.ForeignKey(Contato, on_delete=models.CASCADE, null=True, blank=True)  # Associação com Contato
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['created_at']
        
>>>>>>> 829be17 (Versão CRM GETHOS 1.3 - COM REST API)
