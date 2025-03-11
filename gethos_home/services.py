from .models import Contato
from django.db import transaction

def salvar_contato(dados):
    with transaction.atomic():  # Garante que todos os dados são salvos juntos
        contato = Contato.objects.create(
            nome=dados["nomeCliente"],
            telefone=dados["numeroCliente"],
            nome_animal=dados["nomeAnimal"],
            veterinario_id=dados["veterinarioAtendimento"],
            status=dados["statusAgendamento"],
            data_consulta=dados["dataConsulta"],
            hora_consulta=dados["horaConsulta"],
            tipo_atendimento=dados["tipoAtendimento"],
            observacoes=dados["obsAtendimento"],
        )
        return contato


