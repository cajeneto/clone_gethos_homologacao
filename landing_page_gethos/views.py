from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from gethos_home.models import Contato  # Importa o modelo Contato de gethos_home
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import json

@csrf_exempt
@require_POST
def receber_dados_landing(request):
    try:
        data = json.loads(request.body)
        
        nome = data.get('nome')
        telefone = data.get('telefone')
        email = data.get('email')
        empresa = data.get('empresa', '')
        observacoes = data.get('observacoes', '')
        status = data.get('status', 'Lead')

        if not nome or not telefone or not email:
            return JsonResponse({'success': False, 'message': 'Nome, telefone e e-mail são obrigatórios.'}, status=400)

        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'success': False, 'message': 'E-mail inválido.'}, status=400)

        telefone = telefone.replace(' ', '').replace('-', '')
        if not (len(telefone) == 10 or len(telefone) == 11) or not telefone.isdigit():
            return JsonResponse({'success': False, 'message': 'Telefone inválido. Use o formato 11987654321.'}, status=400)

        contato = Contato(
            nome=nome,
            telefone=telefone,
            email=email,
            empresa=empresa,
            observacoes=observacoes,
            status=status,
            is_deleted=False
        )
        contato.save()

        return JsonResponse({'success': True, 'message': 'Contato salvo com sucesso!'}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Dados inválidos. Envie os dados no formato JSON.'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Erro ao salvar contato: {str(e)}'}, status=500)