from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required

from .models import Contato
from .forms import ContatoForm



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


# @login_required
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


            

    contatos = Contato.objects.all()
    return render(request, 'dashboard_auth.html', {
        'form': form,
        'listContacts': contatos,
    })



# configuração de view para logout de usuário
def logout_view(request):
    logout(request)
    return redirect('home')  # Redireciona para a página de login (ou qualquer outra página) após o logout



# configuração de url para login de administrador
def login_admin(request):
    return HttpResponse('teste login administrador')
 



