from django.db.models.signals import post_save
from django.dispatch import receiver
from gethos_home.models import Contato
from django.core.mail import send_mail
from django.utils.html import strip_tags
import requests
import time

@receiver(post_save, sender=Contato)
def enviar_boas_vindas_contato(sender, instance, created, **kwargs):
    if not created:
        return

    nome = instance.nome
    email_destino = instance.email
    numero_whatsapp = instance.telefone

    print(f"📣 Novo contato: {nome} - {email_destino} - {numero_whatsapp}")

    # === Enviar E-MAIL ===
    if email_destino:
        html_content = f"""
            <h2>Olá, {nome}!</h2>
            <p>Bem-vindo ao <strong>GETHOS CRM</strong>!</p>
            <p>Estamos animados em ter você com a gente! 🚀</p>
        """
        text_content = strip_tags(html_content)

        try:
            send_mail(
                subject="Boas-vindas ao Gethos CRM!",
                message=text_content,
                from_email="Gethos CRM <netocajeh@gmail.com>",
                recipient_list=[email_destino],
                html_message=html_content,
                fail_silently=False
            )
            print("✅ E-mail enviado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao enviar e-mail: {e}")

    # === Enviar WHATSAPP com retry ===
    if numero_whatsapp:
        mensagem = f"Olá {nome}, seja bem-vindo ao GETHOS CRM! 🚀 Conte conosco no que precisar."
    
        payload = {
            "number": numero_whatsapp,
            "text": mensagem
        }
    
        headers = {
            "Content-Type": "application/json",
            "apikey": "zy64iz5z2x8betsuk2rp4r"
        }
    
        for tentativa in range(1, 3):  # Tenta até 2 vezes
            try:
                print(f"💬 Tentando envio do WhatsApp (tentativa {tentativa})...")
                response = requests.post(
                    "https://gethosdev.gethostecnologia.com.br/message/sendText/gethosnotifica",
                    json=payload,
                    headers=headers,
                    timeout=10,
                    verify=False  # ⚠️ IGNORA o erro de SSL (só use se você confiar na API)
                )
                if response.status_code in range(200, 300):
                    print("✅ WhatsApp enviado com sucesso!")
                    break
                else:
                    print(f"❌ Erro WhatsApp: {response.status_code} - {response.text}")
            except requests.exceptions.SSLError as e:
                print(f"⚠️ Erro SSL ao enviar WhatsApp: {e}")
            except Exception as e:
                print(f"❌ Exceção ao enviar WhatsApp: {e}")
    
            time.sleep(3)  # Espera 3 segundos antes de tentar novamente













# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth import get_user_model
# from django.core.mail import send_mail
# from django.utils.html import strip_tags
# from gethos_home.models import Contato


# User = get_user_model()

# @receiver(post_save, sender=Contato)
# def enviar_boas_vindas_contato_novo(sender, instance, created, **kwargs):
#     # Evita duplicidade: dispara só se for recém-criado
#     if not created:
#         return

#     print(f"📣 Novo usuário detectado: {instance.username} - preparando envio...")

#     nome = instance.first_name or instance.username
#     email_destino = instance.email

#     # Envio de e-mail (exatamente como funcionou pra você antes)
#     from django.core.mail import send_mail
#     from django.utils.html import strip_tags

#     html_content = f"""
#         <h2>Olá, {nome}!</h2>
#         <p>Seja muito bem-vindo ao <strong>GETHOS CRM</strong>.</p>
#         <p>Estamos prontos para ajudar você a crescer 🚀</p>
#     """
#     text_content = strip_tags(html_content)

#     try:
#         send_mail(
#             subject="Bem-vindo ao Gethos CRM!",
#             message=text_content,
#             from_email="Gethos CRM <netocajeh@gmail.com>",
#             recipient_list=[email_destino],
#             html_message=html_content,
#             fail_silently=False
#         )
#         print("✅ E-mail de boas-vindas enviado!")
#     except Exception as e:
#         print(f"❌ Erro ao enviar e-mail: {e}")





























# from django.contrib.auth import get_user_model
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.mail import EmailMultiAlternatives
# import requests

# User = get_user_model()

# # Dados da API de WhatsApp
# EVOLUTION_API_URL = "https://gethosdev.gethostecnologia.com.br/message/sendText/gethosnotifica"
# TOKEN = "zy64iz5z2x8betsuk2rp4r"  # mesmo usado no api.py

# @receiver(post_save, sender=User)
# def enviar_boas_vindas_usuario_novo(sender, instance, created, **kwargs):
#     print("🚨 Signal chamado para:", instance.email)

#     if created:
#         nome = instance.first_name or instance.username
#         email_destino = instance.email

#         print(f"✅ Novo usuário criado: {nome} ({email_destino})")

#         # E-MAIl
#         try:
#             assunto = "Bem-vindo(a) ao Gethos CRM!"
#             corpo_texto = "Versão alternativa para leitores antigos."
#             html = f"""
#                 <h2>Olá, {nome}!</h2>
#                 <p>Bem-vindo ao <strong>GETHOS CRM</strong>.</p>
#                 <p>Estamos prontos para te ajudar a crescer 🚀</p>
#             """

#             email = EmailMultiAlternatives(
#                 subject=assunto,
#                 body=corpo_texto,
#                 from_email="Gethos CRM <netocajeh@gmail.com>",
#                 to=[email_destino],
#             )
#             email.attach_alternative(html, "text/html")
#             email.send()
#             print("📧 E-mail enviado com sucesso!")

#         except Exception as e:
#             print(f"❌ Erro ao enviar e-mail: {e}")

#         # WHATSAPP
#         try:
#             mensagem = f"Olá {nome}, seja bem-vindo ao Gethos CRM! 👋"
#             payload = {
#                 "number": "5582991326715",  # Substitua por instance.telefone se existir
#                 "text": mensagem,
#             }
#             headers = {
#                 "Content-Type": "application/json",
#                 "apikey": TOKEN,
#             }
#             response = requests.post(EVOLUTION_API_URL, json=payload, headers=headers, timeout=10)

#             if response.status_code in range(200, 300):
#                 print("💬 WhatsApp enviado com sucesso!")
#             else:
#                 print(f"❌ Erro WhatsApp: {response.status_code} - {response.text}")

#         except Exception as e:
#             print(f"❌ Exceção ao enviar WhatsApp: {e}")
