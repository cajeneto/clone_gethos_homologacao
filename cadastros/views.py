from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from .forms import ModeloMensagemForm, ModeloMensagem



def adicionar_contato(request):
    return render(request, 'cadastro-contato.html')


def visualizar_contato(request):
    return render(request, 'interface-contatos.html')


def cadastro_mensagens(request):
    if request.method == 'POST':
        form = ModeloMensagemForm(request.POST)
        if form.is_valid():
            form.save()  # Salva o formulário se os dados forem válidos
            return redirect('cadastro_mensagens')  # Redireciona após o sucesso
    else:
        form = ModeloMensagemForm()

    return render(request, 'cadastro_mensagens.html', {'form': form})  # Garante que sempre retorna uma resposta HttpResponse



def lista_mensagens_cadastradas(request):
    mensagens = ModeloMensagem.objects.all()  # Busca todas as mensagens no banco
    return render(request, 'lista_mensagens_cadastradas.html', {'mensagens': mensagens})


def detalhe_mensagem_cadastrada(request, id):
    mensagem = get_object_or_404(ModeloMensagem, id=id)  # Obtém a mensagem ou retorna 404
    if request.method == 'POST':
        form = ModeloMensagemForm(request.POST, instance=mensagem)  # Carrega o formulário com os dados da mensagem
        if form.is_valid():
            form.save()  # Salva as alterações
            return redirect('lista_mensagens')  # Redireciona para a lista de mensagens após salvar
    else:
        form = ModeloMensagemForm(instance=mensagem)  # Preenche o formulário com os dados da mensagem

    return render(request, 'detalhe_mensagem_cadastrada.html', {'form': form, 'mensagem': mensagem})