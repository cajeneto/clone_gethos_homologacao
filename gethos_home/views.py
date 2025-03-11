from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
import pandas as pd
from .forms import UploadExcelForm
from .models import Contato, Veterinario, MensagemWhatsApp
from .forms import ContatoForm
from .webScrapingVet import buscar_dados, salvar_dados_no_banco
from .api import enviar_mensagem_api
import asyncio
from .services import salvar_contato
from django.utils.timezone import now
# from .tasks import   # Chamaremos essa função depois
import datetime
from rest_framework import generics
from .models import Contato
from .models import Campanha
from .serializers import ContatoSerializer, CampanhaSerializer
from processos.tasks import enviar_campanha



def home(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # usuario = authenticate(request, acessoUsuario=email, password=password) # valida autenticação

        if email == 'usuario@gethos.com' and password == "senha":
            return redirect('dashboard_auth') #redireciona o usuário para o dashboard_auth (paineil inicial do crm)
        else:
            messages.error(request, 'E-mail ou senha inválidos.')
            return render(request, 'home.html')
    else:
        return render(request, 'home.html')



def create_account(request):
    return render(request, 'create_account.html')









#  TRATA DE ADICIONAR O USUÁRIO NA LISTA DE CONTATOS
# Função para tratar a adição de novos contatos e exibir a lista de contatos
def dashboard_auth(request):
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


    # início de configuração da views dashboard_auth para receber a função de selecionar contatos na lista de contatos.

     # Obtém a lista de IDs dos contatos selecionados no formulário
        selected_contact_ids = request.POST.getlist('selected_contacts')

        if selected_contact_ids:
            # Filtra os contatos selecionados pelo ID
            selected_contacts = Contato.objects.filter(id__in=selected_contact_ids)

            # Aqui você pode realizar a ação desejada com os contatos selecionados
            # Por exemplo, você pode exibir uma mensagem de confirmação
            messages.success(request, f"{selected_contacts.count()} contatos selecionados.")

            # Exemplo: pode redirecionar para uma página de ação
            return redirect('dashboard_auth')  # Mantenha na mesma página, ou redirecione para outra
        
        else:
            # Caso nenhum contato tenha sido selecionado
            messages.error(request, "Nenhum contato foi selecionado.")


    contatos = Contato.objects.all().order_by('-data_criacao')  
    veterinarios = Veterinario.objects.all()  # Adicione esta linha para definir a variável

    print("Contatos encontrados:", contatos)  # Debug para ver os contatos no console

    return render(request, 'dashboard_auth.html', {
        'form': form,
        'listContacts': contatos,
        'veterinarios': veterinarios,
    })



# configuração de view para logout de usuário
def logout_view(request):
    logout(request)
    return redirect('home')  # Redireciona para a página de login (ou qualquer outra página) após o logout


# configuração de url para login de administrador
def login_admin(request):
    return HttpResponse('teste login administrador')
 


def importar_contatos(request):
    if request.method == "POST":
        try:
            # Chama a função do web scraping
            resultado = executar_webscraping(request)
            return JsonResponse({"status": "sucesso", "mensagem": "Importação concluída com sucesso!", "dados": resultado})
        except Exception as e:
            return JsonResponse({"status": "erro", "mensagem": f"Erro ao importar: {str(e)}"})
    return JsonResponse({"status": "falha", "mensagem": "Método inválido."})



# FUNÇÃO PARA REALIZAR LOGIN NO SIMPLES VET

def executar_webscraping(request):
    if request.method == "POST":
        agendamentos = buscar_dados()

        # Salva cada agendamento no banco de dados
        for agendamento in agendamentos:
            salvar_dados_no_banco(agendamento)  # Função já implementada no webScraping.py

        return JsonResponse({"agendamentos": agendamentos})
    return JsonResponse({"erro": "Método não permitido."}, status=405)









@csrf_exempt
def salvar_dados_no_banco(request):
     if request.method == "POST":
        dados = json.loads(request.body)
        contato = salvar_contato(dados)
        return JsonResponse({"message": f"Contato {contato.nome} salvo com sucesso!"}, status=201)








def enviar_mensagem_whatsapp(request):
    
    if request.method == 'POST':
        contato_id = request.POST.get('contato')
        mensagem = request.POST.get('mensagem')
        data_envio = request.POST.get('data_envio')

        contato = Contato.objects.get(id=contato_id)

        if data_envio:
            data_envio = datetime.datetime.strptime(data_envio, "%Y-%m-%dT%H:%M")
        else:
            data_envio = now()

        mensagem_whatsapp = MensagemWhatsApp.objects.create(
            contato=contato,
            mensagem=mensagem,
            data_envio=data_envio,
        )

        if data_envio <= now():
            # CHAMAR A FUNÇÃO DIRETAMENTE (sem Celery)
            resultado = enviar_mensagem_api(mensagem_whatsapp.id)
            print("Resultado do envio:", resultado)

        return redirect('dashboard_auth')

    return redirect('dashboard_auth')








class ContatoListCreate(generics.ListCreateAPIView):
    queryset = Contato.objects.all()
    serializer_class = ContatoSerializer

class ContatoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contato.objects.all()
    serializer_class = ContatoSerializer


class CampanhaListCreateView(generics.ListCreateAPIView):
    queryset = Campanha.objects.all()
    serializer_class = CampanhaSerializer

    def perform_create(self, serializer):
        # Salva a campanha e dispara o envio
        campanha = serializer.save()
        enviar_campanha.delay(campanha.id, intervalo=10)  # Intervalo padrão de 10s
