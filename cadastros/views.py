from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from .forms import ModeloMensagemForm, ModeloMensagem
from .models import Campanha
from .forms import CampanhaForm
from django.contrib import messages
<<<<<<< HEAD
from gethos_home.models import Contato
from gethos_home.forms import ContatoForm
=======
>>>>>>> backup-local



def adicionar_contato(request):
<<<<<<< HEAD
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            print("Formulário válido, salvando contato...")
            form.save()  # Salva o contato
            return redirect('dashboard_auth')  # Redireciona para a mesma página após salvar
        else:
            print("Formulário inválido!")
            print(form.errors)  # Exibe os erros de validação
    else:
        form = ContatoForm()  # Cria um formulário vazio para ser exibido
    contatos = Contato.objects.all().order_by('-data_criacao')

    return render(request, 'cadastro-contato.html', {
        'contato': contatos,
        'form': form,
        })
=======
    return render(request, 'cadastro-contato.html')
>>>>>>> backup-local


def visualizar_contato(request):
    return render(request, 'interface-contatos.html')


def cadastro_mensagens(request):
    if request.method == 'POST':
        form = ModeloMensagemForm(request.POST)
        if form.is_valid():
            form.save()  # Salva o formulário se os dados forem válidos
            return redirect('lista_mensagens_cadastradas')  # Redireciona após o sucesso
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
            return redirect('lista_mensagens_cadastradas')  # Redireciona para a lista de mensagens após salvar
    else:
        form = ModeloMensagemForm(instance=mensagem)  # Preenche o formulário com os dados da mensagem

    return render(request, 'detalhe_mensagem_cadastrada.html', {'form': form, 'mensagem': mensagem})





def nova_campanha(request):
    if request.method == 'POST':
        responsavel = request.POST.get('responsavel')
        titulo = request.POST.get('titulo')
        mensagem_id = request.POST.get('mensagem')
        data_envio = request.POST.get('data')
        hora_envio = request.POST.get('hora')

        if responsavel and titulo and mensagem_id and data_envio and hora_envio:
            mensagem = ModeloMensagem.objects.get(id=mensagem_id)
            Campanha.objects.create(
                responsavel=responsavel,
                titulo=titulo,
                mensagem=mensagem,
                data_envio=data_envio,
                hora_envio=hora_envio
            )
            return redirect('listar_campanhas')
    else:
        mensagens = ModeloMensagem.objects.all()
    
    return render(request, 'nova_campanha.html', {'mensagens': mensagens})


def listar_campanhas(request):
    campanhas = Campanha.objects.all()
    return render(request, 'listar_campanhas.html', {'campanhas': campanhas})


