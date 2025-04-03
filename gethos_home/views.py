from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
# import pandas as pd
from .forms import UploadExcelForm, UsuarioEditForm
from .models import Contato, MensagemWhatsApp
from .forms import ContatoForm
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
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models.signals import post_save



# @login_required
def home(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard_auth')
        else:
            messages.error(request, 'E-mail ou senha inválidos.')
            return render(request, 'home.html')
    else:
        # Consumir mensagens antigas, exceto as de login
        storage = get_messages(request)
        for message in storage:
            if 'E-mail ou senha inválidos' not in str(message):
                storage.used = True  # Marca as mensagens como usadas
        return render(request, 'home.html')



def create_account(request):
    return render(request, 'create_account.html')


#  TRATA DE ADICIONAR O LEAD NA LISTA DE CONTATOS
# Função para tratar a adição de novos contatos e exibir a lista de contatos

@login_required
def dashboard_auth(request):
    form = ContatoForm()

    if request.method == 'POST':
        if 'adicionar_contato' in request.POST:
            form = ContatoForm(request.POST)
            if form.is_valid():
                print("Formulário válido, salvando contato...")
                
                # Captura os valores dos checkboxes
                enviar_email = request.POST.get("enviar_email") == "on"
                enviar_whatsapp = request.POST.get("enviar_whatsapp") == "on"

                # Salva o contato e obtém a instância
                contato = form.save()

                # Dispara o signal manualmente com os argumentos extras
                post_save.send(
                    sender=Contato,
                    instance=contato,
                    created=True,
                    enviar_email=enviar_email,
                    enviar_whatsapp=enviar_whatsapp
                )

                messages.success(request, 'Contato adicionado com sucesso!')
                return redirect('dashboard_auth')
            else:
                print("Formulário inválido!")
                print(form.errors)
                messages.error(request, 'Erro ao adicionar contato. Verifique os dados.')

            # Nova ação para configurar o webhook
        elif 'configurar_webhook' in request.POST:
            from configuracoes.models import APIEvoGetInstance
            instancia = APIEvoGetInstance.objects.first()
            if not instancia:
                messages.error(request, "Nenhuma instância de WhatsApp configurada!")
                return redirect('dashboard_auth')

            url = "https://gethosdev.gethostecnologia.com.br/instance/setWebhook"
            payload = {
                "instanceName": instancia.instance_name,
                "webhook": {
                    "url": "https://app.gethostecnologia.com.br/webhook/",  # Substitua pelo seu URL público
                    "webhook_by_events": False,
                    "events": ["MESSAGES_UPSERT"]
                }
            }
            headers = {
                "Content-Type": "application/json",
                "apikey": "94fc6ec0af7a6564824bc8df4be618c4246d36f2"  # API Key da Evolution
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                messages.success(request, "Webhook configurado com sucesso!")
            else:
                messages.error(request, f"Erro ao configurar webhook: {response.text}")
            return redirect('dashboard_auth')








        # Verifica se o formulário é para selecionar contatos
        elif 'selecionar_contatos' in request.POST:
            selected_contact_ids = request.POST.getlist('selected_contacts')
            if selected_contact_ids:
                selected_contacts = Contato.objects.filter(id__in=selected_contact_ids, is_deleted=False)
                messages.success(request, f"{selected_contacts.count()} contatos selecionados.")
                return redirect('dashboard_auth')
            else:
                messages.error(request, "Nenhum contato foi selecionado.")

    contatos = Contato.objects.filter(is_deleted=False).order_by('-data_criacao')

    print("Contatos encontrados:", contatos)

    return render(request, 'dashboard_auth.html', {
        'form': form,
        'listContacts': contatos,
    })

# Endpoint para receber webhooks
@csrf_exempt
def whatsapp_webhook(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            event = body.get('event')
            data = body.get('data', {})

            if event == 'MESSAGES_UPSERT':
                message_data = data.get('message', {})
                sender = data.get('key', {}).get('remoteJid')  # Número do cliente (ex.: 5511999999999@s.whatsapp.net)
                is_from_me = data.get('key', {}).get('fromMe', False)

                # Extrair mensagem recebida
                message_text = None
                if 'conversation' in message_data:
                    message_text = message_data['conversation']
                elif 'extendedTextMessage' in message_data:
                    message_text = message_data['extendedTextMessage'].get('text')

                if message_text and not is_from_me:
                    print(f"📩 Mensagem recebida de {sender}: {message_text}")
                    
                    # Resposta automática
                    resposta = f"Olá! Recebemos sua mensagem: '{message_text}'. Como posso ajudar você hoje?"
                    from configuracoes.models import APIEvoGetInstance
                    instancia = APIEvoGetInstance.objects.first()
                    if not instancia:
                        return JsonResponse({'status': 'error', 'message': 'Nenhuma instância configurada'}, status=500)

                    url = f"https://gethosdev.gethostecnologia.com.br/message/sendText/{instancia.instance_name}"
                    payload = {
                        "number": sender.split('@')[0],  # Remove @s.whatsapp.net
                        "text": resposta
                    }
                    headers = {
                        "Content-Type": "application/json",
                        "apikey": instancia.api_key
                    }
                    response = requests.post(url, json=payload, headers=headers)
                    if response.status_code == 200:
                        print(f"✅ Resposta enviada para {sender}: {resposta}")
                    else:
                        print(f"❌ Erro ao enviar resposta: {response.text}")

            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            print(f"❌ Erro no webhook: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)





















# configuração de view para logout de usuário
def logout_view(request):
    logout(request)
    return redirect('home')  # Redireciona para a página de login após o logout


# configuração de url para login de administrador
def login_admin(request):
    return HttpResponse('teste login administrador')
 






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



class CampanhaListCreateView(generics.ListCreateAPIView):
    queryset = Campanha.objects.all()
    serializer_class = CampanhaSerializer


class ContatoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contato.objects.all()
    serializer_class = ContatoSerializer

    def perform_create(self, serializer):
        # Salva a campanha e dispara o envio
        campanha = serializer.save()
        enviar_campanha.delay(campanha.id, intervalo=10)  # Intervalo padrão de 10s




@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = UsuarioEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('editar_perfil')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = UsuarioEditForm(instance=request.user)
    return render(request, 'editar_perfil.html', {'form': form})





@login_required
def editar_contato(request, contato_id):
    contato = get_object_or_404(Contato, id=contato_id, is_deleted=False)
    
    if request.method == 'POST':
        form = ContatoForm(request.POST, instance=contato)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contato atualizado com sucesso!')
            return redirect('dashboard_auth')
        else:
            messages.error(request, 'Erro ao atualizar contato. Verifique os dados.')
    else:
        form = ContatoForm(instance=contato)
    
    return render(request, 'editar_contato.html', {
        'form': form,
        'contato': contato,
    })



@login_required
def excluir_contato(request, contato_id):
    contato = get_object_or_404(Contato, id=contato_id, is_deleted=False)
    if request.method == 'POST':
        contato.is_deleted = True
        contato.save()
        messages.success(request, 'Contato excluído com sucesso!')
        return redirect('dashboard_auth')
    return render(request, 'confirmar_exclusao.html', {'contato': contato})






@login_required
@staff_member_required
def contatos_excluidos(request):
    contatos = Contato.objects.filter(is_deleted=True).order_by('-data_criacao')
    return render(request, 'contatos_excluidos.html', {'contatos': contatos})



