from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone  # Import correto para timezone
import gethos_home
from .models import FluxoCaptacao, StatusKanban
from gethos_home.models import Contato, MensagemWhatsApp, Campanha
from gethos_home.api import enviar_mensagem_api
import json
from processos.tasks import enviar_campanha
from django.contrib import messages


def fluxo_captacao(request):
    status_list = StatusKanban.objects.all()
    contatos = Contato.objects.all()

    # Cria um dicionário com etapas agrupadas por status
    etapas_por_status = {}
    for status in status_list:
        etapas = FluxoCaptacao.objects.filter(status=status.nome).select_related('contato')
        etapas_por_status[status.nome] = etapas

    return render(request, 'fluxo_captacao.html', {
        'status_list': status_list,
        'etapas_por_status': etapas_por_status,
        'contatos': contatos
    })

@csrf_exempt
def move_task(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        task_id = data.get('task_id')
        new_status = data.get('new_status')

        task = get_object_or_404(FluxoCaptacao, id=task_id)
        status_obj = StatusKanban.objects.get(nome=new_status)  # Busca o objeto StatusKanban
        task.etapa = status_obj  # Atribui o objeto ao campo 'etapa'
        task.save()

        if new_status == 'Em andamento' and task.contato:
            msg = gethos_home.models.MensagemWhatsApp.objects.create(
                contato=task.contato,
                mensagem="Movido para Em andamento",
                data_envio=timezone.now()
            )
            enviar_mensagem_api.delay(msg.id)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def add_etapa(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        status_nome = request.POST.get('status', 'A fazer')
        contato_id = request.POST.get('contato')
        contato = Contato.objects.get(id=contato_id) if contato_id else None
        status_obj = StatusKanban.objects.get(nome=status_nome)  # Busca o objeto StatusKanban pelo nome
        FluxoCaptacao.objects.create(titulo=titulo, etapa=status_obj, contato=contato)  # Usa 'etapa' e passa o objeto
        return redirect('fluxo_captacao')
    contatos = Contato.objects.all()
    return render(request, 'add_etapa.html', {'contatos': contatos})

def edit_etapa(request, id_etapa):
    etapa = get_object_or_404(FluxoCaptacao, id=id_etapa)
    if request.method == 'POST':
        etapa.titulo = request.POST.get('titulo')
        etapa.descricao = request.POST.get('descricao')
        etapa.status = request.POST.get('status')
        etapa.contato = Contato.objects.get(id=request.POST.get('contato')) if request.POST.get('contato') else None
        etapa.save()
        return redirect('fluxo_captacao')
    contatos = Contato.objects.all()
    return render(request, 'edit_etapa.html', {'etapa': etapa, 'contatos': contatos})

def delete_etapa(request, id_etapa):
    etapa = get_object_or_404(FluxoCaptacao, id=id_etapa)
    etapa.delete()
    return redirect('fluxo_captacao')

def enviar_mensagem(request):
    if request.method == 'POST':
        nome_campanha = request.POST.get('nome_campanha')
        mensagem = request.POST.get('mensagem')
        contatos_ids = request.POST.getlist('contatos')  # Aq lista os ids
        intervalo = int(request.POST.get('intervalo', 10))  # intervalo de mensagem, padrão 10 segundos.
        # contatos = Contato.objects.filter(id__in=contatos_ids)

        if not contatos_ids:
            messages.error(request, "Selecione pelo menos um contato para a campanha.")
            return render(request, 'enviar_mensagem.html', {'contato': Contato.objects.all()})

        contatos = Contato.objects.filter(id__in=contatos_ids)
        try:
            campanha = Campanha.objects.create(
                nome=nome_campanha,
                mensagem=mensagem
            )
            campanha.contatos.set(contatos)
            enviar_campanha.delay(campanha.id, intervalo)
            messages.success(request, f"Campanha '{nome_campanha}' criada e enviada com sucesso!")
            return redirect('enviar_mensagem')
        except Exception as e:
            messages.error(request, f"Erro ao criar campanha: {str(e)}")
            return render(request, 'enviar_mensagem.html', {'contato': Contato.objects.all()})

    contatos = Contato.objects.all()
    return render(request, 'enviar_mensagem.html', {'contato': contatos})
       

# PENDENTE DE TESTES
def relatorios(request):
    campanhas = Campanha.objects.all().prefetch_related('mensagemwhatsapp_set')  # Agora válido
    relatorio = []
    for campanha in campanhas:
        total_contatos = campanha.contatos.count()
        mensagens_enviadas = campanha.mensagemwhatsapp_set.filter(enviado=True).count()
        mensagens_falhas = campanha.mensagemwhatsapp_set.filter(enviado=False).count()
        relatorio.append({
            'nome': campanha.nome,
            'total_contatos': total_contatos,
            'mensagens_enviadas': mensagens_enviadas,
            'mensagens_falhas': mensagens_falhas,
            'status': campanha.status,
        })
    return render(request, 'relatorios.html', {'relatorio': relatorio})
       
       
@csrf_exempt
def criar_etapa_ajax(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        contato_id = request.POST.get('contato_id')
        status_nome = request.POST.get('status')

        try:
            contato = Contato.objects.get(id=contato_id)
            status_obj = StatusKanban.objects.get(nome=status_nome)
            FluxoCaptacao.objects.create(
                titulo=titulo,
                contato=contato,
                etapa=status_obj  # Corrigido: usa 'etapa' e passa o objeto
            )
            return JsonResponse({'sucesso': True})
        except Exception as e:
            return JsonResponse({'erro': str(e)})
       
       
       
       
       
       
       
       
       
""" # Criar a campanha
        campanha = Campanha.objects.create(
            nome=nome_campanha,
            mensagem=mensagem
        )
        campanha.contatos.set(contatos)

        # Disparar envio assíncrono
        enviar_campanha.delay(campanha.id, intervalo)

        return redirect('fluxo_captacao')

    contatos = Contato.objects.all()
    return render(request, 'enviar_mensagem.html', {'contato': contatos}) 
"""
