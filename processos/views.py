from django.shortcuts import render, redirect, get_object_or_404
from .models import FluxoCaptacao
from gethos_home.models import Contato
from cadastros.models import ModeloMensagem, Campanha




# View principal de visualização de tarefas (dashboard)
def fluxo_captacao(request):
    fluxo_a_fazer = FluxoCaptacao.objects.filter(status='A fazer')
    fluxo_progresso = FluxoCaptacao.objects.filter(status='Em andamento')
    fluxo_concluido = FluxoCaptacao.objects.filter(status='Concluído')

    return render(request, 'fluxo_captacao.html', {
        'fluxo_a_fazer': fluxo_a_fazer,
        'fluxo_progresso': fluxo_progresso,
        'fluxo_concluido': fluxo_concluido,
    })


# View para adicionar etapa dentro de um fluxo
def add_etapa(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        status = request.POST.get('status', 'A fazer')  # Padrão: 'A fazer'
        FluxoCaptacao.objects.create(titulo=titulo, descricao=descricao, status=status)
        return redirect('fluxo_captacao')

    return render(request, 'add_etapa.html')


# View para editar uma etapa
def edit_etapa(request, id_etapa):
    etapa = get_object_or_404(FluxoCaptacao, id=id_etapa)

    if request.method == 'POST':
        etapa.titulo = request.POST.get('titulo')
        etapa.descricao = request.POST.get('descricao')
        etapa.status = request.POST.get('status')
        etapa.save()
        return redirect('fluxo_captacao')

    return render(request, 'edit_etapa.html', {'etapa': etapa})



# View para excluir uma etapa
def delete_etapa(request, id_etapa):
    etapa = get_object_or_404(FluxoCaptacao, id=id_etapa)
    etapa.delete()
    return redirect('fluxo_captacao')



def enviar_mensagem(request):
    contatos = Contato.objects.all()  # Consulta todos os contatos cadastrados
    mensagens = ModeloMensagem.objects.all()
    campanhas = Campanha.objects.all()

    return render(request, 'enviar_mensagem.html', 
                  { 'contato': contatos, 
                   'mensagens' : mensagens,
                   'campanhas': campanhas
                   } )