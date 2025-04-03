from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from .forms import ModeloMensagemForm, ModeloMensagem
from .models import Campanha, FluxoAutomatizado, EtapaFluxo, ExecucaoFluxo
from .forms import CampanhaForm, FluxoAutomatizadoForm, EtapaFluxoForm
from django.contrib import messages
from gethos_home.models import Contato
from gethos_home.forms import ContatoForm
from django.core.mail import EmailMultiAlternatives
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from cadastros.tasks import iniciar_execucao_fluxo
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect
import json
from .models import MensagemWhatsApp
from .services.whatsapp_service import enviar_mensagem_evolution_service  # vamos criar esse depois
from django.urls import reverse


def adicionar_contato(request):
    
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


def visualizar_contato(request):
    return render(request, 'interface-contatos.html')

def cadastro_mensagens(request):
    if request.method == 'POST':
        print("=== HTML vindo do Unlayer ===")
        print(request.POST.get('conteudo_mensagem')) 

        data = request.POST.copy()
        form = ModeloMensagemForm(data)
        print("📦 Todos os dados POST:", request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Mensagem salva com sucesso!")
            return redirect('lista_mensagens_cadastradas')
        else:
            print("Formulário inválido:", form.errors)
    else:
        form = ModeloMensagemForm()

    return render(request, 'cadastro_mensagens.html', {
    'form': form,
    'mensagem': None  # <- assim evita erro ao acessar {{ mensagem }} no template
})


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




def enviar_email_html(request):
    contatos = Contato.objects.all()
    modelos = ModeloMensagem.objects.filter(tipo_mensagem=3)  # Tipo 3 = Email

    if request.method == 'POST':
        modelo_id = request.POST.get('modelo')
        contatos_ids = request.POST.getlist('contatos')
        assunto = request.POST.get('assunto')

        modelo = ModeloMensagem.objects.get(id=modelo_id)
        contatos_selecionados = Contato.objects.filter(id__in=contatos_ids)

        for contato in contatos_selecionados:
            email = contato.email
            nome = contato.nome
            html_content = modelo.conteudo_mensagem.replace("@nome", nome)

            email_msg = EmailMultiAlternatives(
                subject=assunto,
                body="Versão alternativa para leitores antigos.",
                from_email="seuemail@dominio.com",
                to=[email]
            )
            email_msg.attach_alternative(html_content, "text/html")
            email_msg.send()

        messages.success(request, "E-mails enviados com sucesso.")
        return redirect('enviar_email_html')

    return render(request, 'enviar_email_html.html', {
        'modelos': modelos,
        'contatos': contatos
    })







def clonar_mensagem(request, id):
    original = get_object_or_404(ModeloMensagem, id=id)

    # Cria uma cópia não salva
    clone = ModeloMensagem(
        nome_modelo=f"{original.nome_modelo} (cópia)",
        tipo_mensagem=original.tipo_mensagem,
        conteudo_mensagem=original.conteudo_mensagem
    )
    clone.save()

    messages.success(request, "Modelo clonado com sucesso!")
    return redirect('lista_mensagens_cadastradas')




def lista_fluxos_automacao(request):
    fluxos = FluxoAutomatizado.objects.all().order_by('-criado_em')
    return render(request, 'fluxo_automacao_gethos.html', {'fluxos': fluxos})


def novo_fluxo_automacao(request):
    mensagens = ModeloMensagem.objects.all()

    if request.method == 'POST':
        form = FluxoAutomatizadoForm(request.POST)
        if form.is_valid():
            fluxo = form.save()

            etapas_raw = [key for key in request.POST if key.startswith("etapas-") and key.endswith("-ordem")]
            total_etapas = len(etapas_raw)

            for i in range(total_etapas):
                ordem = request.POST.get(f'etapas-{i}-ordem')
                canal = request.POST.get(f'etapas-{i}-canal')
                mensagem_id = request.POST.get(f'etapas-{i}-mensagem')
                delay_intervalo = request.POST.get(f'etapas-{i}-delay_intervalo')  # Novo campo
                intervalo_tipo = request.POST.get(f'etapas-{i}-intervalo_tipo')    # Novo campo

                if ordem and canal and mensagem_id and delay_intervalo and intervalo_tipo:
                    EtapaFluxo.objects.create(
                        fluxo=fluxo,
                        ordem=int(ordem),
                        canal=canal,
                        mensagem_id=int(mensagem_id),
                        delay_intervalo=int(delay_intervalo),
                        intervalo_tipo=intervalo_tipo
                    )

            return redirect('lista_fluxos_automacao')
    else:
        form = FluxoAutomatizadoForm()

    return render(request, 'novo_fluxo_automacao.html', {
        'form': form,
        'mensagens': mensagens,
        'etapas': []
    })





def adicionar_etapas_fluxo(request, fluxo_id):
    fluxo = get_object_or_404(FluxoAutomatizado, id=fluxo_id)
    etapas = fluxo.etapas.order_by('ordem')

    if request.method == 'POST':
        form = EtapaFluxoForm(request.POST)
        if form.is_valid():
            etapa = form.save(commit=False)
            etapa.fluxo = fluxo
            etapa.save()
            return redirect('adicionar_etapas_fluxo', fluxo_id=fluxo.id)
    else:
        form = EtapaFluxoForm()

    return render(request, 'adicionar_etapas_fluxo.html', {
        'fluxo': fluxo,
        'etapas': etapas,
        'form': form
    })




def visualizar_fluxo_automacao(request, fluxo_id):
    fluxo = get_object_or_404(FluxoAutomatizado, id=fluxo_id)
    etapas = fluxo.etapas.order_by('ordem')

    return render(request, 'visualizar_fluxo_automacao.html', {
        'fluxo': fluxo,
        'etapas': etapas
    })




def editar_fluxo_automacao(request, fluxo_id):
    fluxo = get_object_or_404(FluxoAutomatizado, id=fluxo_id)
    etapas = fluxo.etapas.order_by('ordem')
    mensagens = ModeloMensagem.objects.all()

    if request.method == 'POST':
        form = FluxoAutomatizadoForm(request.POST, instance=fluxo)
        if form.is_valid():
            form.save()

            # Limpa e recria etapas
            fluxo.etapas.all().delete()

            etapas_raw = [k for k in request.POST if k.startswith("etapas-") and k.endswith("-ordem")]
            total_etapas = len(etapas_raw)

            for i in range(total_etapas):
                ordem = request.POST.get(f'etapas-{i}-ordem')
                canal = request.POST.get(f'etapas-{i}-canal')
                mensagem_id = request.POST.get(f'etapas-{i}-mensagem')
                delay_intervalo = request.POST.get(f'etapas-{i}-delay_intervalo')  # campo novo
                intervalo_tipo = request.POST.get(f'etapas-{i}-intervalo_tipo')    # campo novo

                if ordem and canal and mensagem_id and delay_intervalo and intervalo_tipo:
                    EtapaFluxo.objects.create(
                        fluxo=fluxo,
                        ordem=int(ordem),
                        canal=canal,
                        mensagem_id=int(mensagem_id),
                        delay_intervalo=int(delay_intervalo),
                        intervalo_tipo=intervalo_tipo
                    )

            return redirect('lista_fluxos_automacao')
    else:
        form = FluxoAutomatizadoForm(instance=fluxo)

    return render(request, 'novo_fluxo_automacao.html', {
        'form': form,
        'fluxo': fluxo,
        'etapas': etapas,
        'mensagens': mensagens,
        'edicao': True
    })





@api_view(['POST'])
def cadastro_landing_page(request):
    nome = request.data.get("nome")
    telefone = request.data.get("telefone")
    email = request.data.get("email")

    if not nome or not telefone or not email:
        return Response({"erro": "Dados incompletos!"}, status=status.HTTP_400_BAD_REQUEST)

    contato, created = Contato.objects.get_or_create(
        email=email,
        defaults={"nome": nome, "telefone": telefone}
    )

    fluxo_nome = "Transforme Leads em Clientes com Nosso CRM"
    try:
        fluxo = FluxoAutomatizado.objects.get(nome=fluxo_nome)
    except FluxoAutomatizado.DoesNotExist:
        return Response({"erro": f"Fluxo '{fluxo_nome}' não encontrado."}, status=status.HTTP_404_NOT_FOUND)

    execucao = ExecucaoFluxo.objects.create(contato=contato, fluxo=fluxo)
    iniciar_execucao_fluxo.delay(execucao.id)

    return Response({"status": "Contato salvo e fluxo iniciado!"}, status=status.HTTP_201_CREATED)










# TRATA DE RECEBER MENSAGENS DO WHATSAPP VIA WEBHOOK.

@csrf_exempt
def webhook_receber_mensagem(request):
    if request.method != "POST":
        return JsonResponse({"erro": "Método não permitido"}, status=405)

    try:
        data = json.loads(request.body)
        telefone = data.get("phone")  # ou "numbr", conforme a Evolution
        mensagem = data.get("message")

        if not telefone or not mensagem:
            return JsonResponse({"erro": "Dados incompletos"}, status=400)

        # Verifica se o contato existe
        contato, criado = Contato.objects.get_or_create(
            telefone=telefone,
            defaults={"nome": "Desconhecido", "email": ""}
        )

        # Salva a mensagem como "recebida"
        MensagemWhatsApp.objects.create(
            contato=contato,
            mensagem=mensagem,
            enviado=True,  # foi recebido pelo sistema
            tipo="recebida"  # você pode adicionar esse campo se quiser
        )

        print(f"📩 Mensagem recebida de {telefone}: {mensagem}")
        return JsonResponse({"status": "ok"})

    except json.JSONDecodeError:
        return JsonResponse({"erro": "JSON inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=500)
    

# TRATA DA CENTRAL DO WHATSAPP COM AS MENSAGENS DO WHATSAPP.

@csrf_exempt
def central_whatsapp_chat(request, contato_id=None):
    contatos = Contato.objects.order_by('nome')
    contato = None
    mensagens = []

    if contato_id:
        contato = get_object_or_404(Contato, id=contato_id)
        mensagens = MensagemWhatsApp.objects.filter(contato=contato).order_by('data_criacao')

    return render(request, 'central_whatsapp_chat.html', {
        'contatos': contatos,
        'contato': contato,
        'mensagens': mensagens
    })



def mensagens_json(request, contato_id):
    mensagens = MensagemWhatsApp.objects.filter(contato_id=contato_id).order_by('data_criacao')
    data = [
        {
            'mensagem': m.mensagem,
            'tipo': m.tipo,
            'data': m.data_criacao.strftime('%d/%m %H:%M')
        }
        for m in mensagens
    ]
    return JsonResponse({'mensagens': data})


def enviar_mensagem_whatsapp(request, contato_id):
    if request.method == 'POST':
        mensagem = request.POST.get('mensagem')
        contato = get_object_or_404(Contato, id=contato_id)

        if mensagem:
            # envia pela Evolution
            enviar_mensagem_evolution_service(contato.telefone, mensagem)

            # salva no histórico
            MensagemWhatsApp.objects.create(
                contato=contato,
                mensagem=mensagem,
                tipo='enviada',
                enviado=True
            )
    return redirect('central_whatsapp_chat', contato_id=contato_id)