from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from .forms import ConfigFormEmpresa
from .models import CadastroEmpresa, EmailSMTPUsuario, APIEvoUsuario, APIEvoGetInstance
import requests
import json
import qrcode
from io import BytesIO
import base64
from django.template.loader import render_to_string

@login_required
def configuracoes_view(request):
    try:
        empresa = CadastroEmpresa.objects.first()
        email_smtp = EmailSMTPUsuario.objects.first()
        api_evo = APIEvoUsuario.objects.first()
        instancia = APIEvoGetInstance.objects.first()
    except CadastroEmpresa.DoesNotExist:
        empresa = None
        email_smtp = None
        api_evo = None
        instancia = None

    status_data = None
    error_message = None
    if instancia:
        url = f"https://gethosdev.gethostecnologia.com.br/instance/connect/{instancia.instance_name}"
        headers = {"apikey": instancia.api_key}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            status_data = response.json()
        except requests.exceptions.RequestException as e:
            error_message = f"Erro ao conectar com a API: {str(e)}"

    if request.method == 'POST':
        if 'gerar_qr_code' in request.POST:
            whatsapp_nome = request.POST.get('whatsapp_nome')
            whatsapp_numero = request.POST.get('whatsapp_numero')

            # Exclui a instância existente, se houver
            if instancia:
                url_delete = f"https://gethosdev.gethostecnologia.com.br/instance/delete/{instancia.instance_name}"
                headers_delete = {"apikey": "94fc6ec0af7a6564824bc8df4be618c4246d36f2"}
                try:
                    response = requests.delete(url_delete, headers=headers_delete)
                    response.raise_for_status()
                    instancia.delete()  # Remove do banco local após sucesso na API
                except requests.exceptions.RequestException as e:
                    # Se der erro (ex.: 404), continua para criar a nova instância
                    print(f"Erro ao excluir instância antiga: {str(e)}")
                    instancia.delete()  # Remove do banco mesmo assim para evitar duplicatas locais

            # Cria a nova instância
            url_create = "https://gethosdev.gethostecnologia.com.br/instance/create"
            payload = json.dumps({
                "instanceName": whatsapp_nome,
                "qrcode": True,
                "token": whatsapp_nome + 'CRM',
                "number": whatsapp_numero,
                "integration": "WHATSAPP-BAILEYS",
            })
            headers_create = {
                'Content-Type': 'application/json',
                'apikey': '94fc6ec0af7a6564824bc8df4be618c4246d36f2'
            }

            response = requests.post(url_create, headers=headers_create, data=payload)
            data = response.json()
            qr_code_data = data.get('qrcode', {}).get('code', '')

            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr.add_data(qr_code_data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            qr_code_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            qr_code_url = f"data:image/png;base64,{qr_code_base64}"

            # Salva a nova instância (substituindo qualquer anterior)
            APIEvoGetInstance.objects.all().delete()  # Garante que só haja uma instância no banco
            nova_instancia = APIEvoGetInstance(
                instance_name=whatsapp_nome,
                api_key=whatsapp_nome + 'CRM',
                qr_code_data=qr_code_url,
                state='open'
            )
            nova_instancia.save()

            return JsonResponse({'qr_code': qr_code_url})

        if 'excluir_instancia' in request.POST:
            if instancia:
                url = f"https://gethosdev.gethostecnologia.com.br/instance/delete/{instancia.instance_name}"
                headers = {"apikey": "94fc6ec0af7a6564824bc8df4be618c4246d36f2"}
                try:
                    response = requests.delete(url, headers=headers)
                    response.raise_for_status()
                    instancia.delete()
                    return JsonResponse({'success': 'Instância excluída com sucesso!'})
                except requests.exceptions.RequestException as e:
                    return JsonResponse({'error': f"Erro ao excluir instância: {str(e)}"}, status=400)
            return JsonResponse({'error': 'Nenhuma instância encontrada para excluir'}, status=404)

        if empresa:
            form = ConfigFormEmpresa(request.POST, instance=empresa)
        else:
            form = ConfigFormEmpresa(request.POST)

        if form.is_valid():
            empresa = form.save(commit=False)
            empresa.save()

            if email_smtp:
                email_smtp.email_usuario = form.cleaned_data['email_usuario']
                email_smtp.chave_api_secret_usuario = form.cleaned_data['api_key']
                email_smtp.remetente_email_usuario = form.cleaned_data['remetente']
                email_smtp.save()
            else:
                email_smtp = EmailSMTPUsuario(
                    email_usuario=form.cleaned_data['email_usuario'],
                    chave_api_secret_usuario=form.cleaned_data['api_key'],
                    remetente_email_usuario=form.cleaned_data['remetente'],
                    servidor_smtp_usuario="smtp.gmail.com",
                    porta_smtp_usuario=587,
                    usa_tls_usuario=True
                )
                email_smtp.save()

            if api_evo:
                api_evo.telefone_usuario_api = form.cleaned_data['whatsapp_numero']
                api_evo.nome_conexao = form.cleaned_data['whatsapp_nome']
                api_evo.save()
            else:
                api_evo = APIEvoUsuario(
                    telefone_usuario_api=form.cleaned_data['whatsapp_numero'],
                    nome_conexao=form.cleaned_data['whatsapp_nome'],
                    ativo=True
                )
                api_evo.save()

            messages.success(request, 'Configurações salvas com sucesso!')
            return redirect('dashboard_auth')
    else:
        if empresa:
            initial_data = {
                'email_usuario': email_smtp.email_usuario if email_smtp else '',
                'api_key': email_smtp.chave_api_secret_usuario if email_smtp else '',
                'remetente': email_smtp.remetente_email_usuario if email_smtp else '',
                'whatsapp_nome': api_evo.nome_conexao if api_evo else '',
                'whatsapp_numero': api_evo.telefone_usuario_api if api_evo else '',
            }
            form = ConfigFormEmpresa(instance=empresa, initial=initial_data)
        else:
            form = ConfigFormEmpresa()

    context = {
        'form': form,
        'instancia': instancia,
        'status_data': status_data,
        'error': error_message,
    }
    return render(request, 'configuracoes.html', context)



# Nova view para atualizar o fieldset WhatsApp
@login_required
def atualizar_whatsapp_view(request):
    instancia = APIEvoGetInstance.objects.first()
    api_evo = APIEvoUsuario.objects.first()
    status_data = None
    error_message = None

    if instancia:
        url = f"https://gethosdev.gethostecnologia.com.br/instance/connectionState/{instancia.instance_name}"
        headers = {"apikey": instancia.api_key}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            status_data = response.json()
        except requests.exceptions.RequestException as e:
            error_message = f"Erro ao conectar com a API: {str(e)}"

    form = ConfigFormEmpresa(request.POST or None, initial={
        'whatsapp_nome': api_evo.nome_conexao if api_evo else '',
        'whatsapp_numero': api_evo.telefone_usuario_api if api_evo else '',
    })

    context = {
        'form': form,
        'instancia': instancia,
        'status_data': status_data,
        'error': error_message,
    }
    html = render_to_string('whatsapp_fieldset.html', context)
    return HttpResponse(html)




