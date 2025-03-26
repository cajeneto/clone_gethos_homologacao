from .models import Contato
from django.db import transaction

def salvar_contato(dados):
    with transaction.atomic():  # Garante que todos os dados são salvos juntos
        contato = Contato.objects.create(
            nome=dados["nomeCliente"],
            telefone=dados["numeroCliente"],
            observacoes=dados["obsAtendimento"],
        )
        return contato


