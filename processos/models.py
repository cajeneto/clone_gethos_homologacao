from django.db import models
from gethos_home.models import Contato


class StatusKanban(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome


def get_default_status():
    """Retorna o ID do StatusKanban 'A fazer', criando-o se necessário."""
    status, _ = StatusKanban.objects.get_or_create(nome='A fazer')
    return status.id


class FluxoCaptacao(models.Model):
    titulo = models.CharField(max_length=100)
    etapa = models.ForeignKey(
        StatusKanban,
        on_delete=models.CASCADE,
        default=get_default_status
    )
    contato = models.ForeignKey(Contato, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.contato.nome} em {self.etapa.nome}"