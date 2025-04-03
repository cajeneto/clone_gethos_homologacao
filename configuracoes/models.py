from django.db import models
import json


# Tabela CadastroEmpresa
class CadastroEmpresa(models.Model):
    nome_empresa = models.CharField(max_length=255)
    cnpj_empresa = models.CharField(max_length=18, unique=True)  # Ex: 12.345.678/0001-99
    rua_empresa = models.CharField(max_length=255)
    cep_empresa = models.CharField(max_length=9)  # Ex: 12345-678
    telefone_empresa = models.CharField(max_length=15)  # Ex: (11) 98765-4321
    bairro_empresa = models.CharField(max_length=100, blank=True, null=True)
    cidade_empresa = models.CharField(max_length=100)
    estado_empresa = models.CharField(max_length=2)  # Ex: SP, RJ
    email_contato_empresa = models.EmailField(blank=True, null=True)
    data_criacao_user_empresa = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
    


# Tabela EmailSMTPUsuario
class EmailSMTPUsuario(models.Model):
    email_usuario = models.EmailField(unique=True)
    chave_api_secret_usuario = models.CharField(max_length=255)  # Para armazenar a senha ou chave API
    remetente_email_usuario = models.EmailField()
    servidor_smtp_usuario = models.CharField(max_length=100, default="smtp.gmail.com")  # Exemplo
    porta_smtp_usuario = models.IntegerField(default=587)
    usa_tls_usuario = models.BooleanField(default=True)
    data_atualizacao_usuario = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email_usuario
    

# Tabela APIEvoUsuario
class APIEvoUsuario(models.Model):
    telefone_usuario_api = models.CharField(max_length=15, unique=True)  # Ex: +5511987654321
    nome_conexao = models.CharField(max_length=100)
    data_conexao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome_conexao} ({self.telefone_usuario_api})"
    

# Tabela APIEvoGetInstance
class APIEvoGetInstance(models.Model):
    instance_name = models.CharField(max_length=100, unique=True)
    state = models.CharField(max_length=50, default="open")
    api_key = models.CharField(max_length=255)
    qr_code_data = models.TextField(blank=True, null=True)  # Armazena o QR code ou URL
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.instance_name


