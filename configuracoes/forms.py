from django import forms
from .models import CadastroEmpresa, EmailSMTPUsuario, APIEvoUsuario

class ConfigFormEmpresa(forms.ModelForm):
    # Campos adicionais que não estão diretamente no CadastroEmpresa
    email_usuario = forms.EmailField(label="Email do Usuário")
    api_key = forms.CharField(label="Chave API Google")
    remetente = forms.EmailField(label="Remetente do Email")
    whatsapp_nome = forms.CharField(label="Nome do WhatsApp", max_length=100)
    whatsapp_numero = forms.CharField(label="Número do WhatsApp", max_length=15)

    class Meta:
        model = CadastroEmpresa
        fields = [
            'nome_empresa', 'cnpj_empresa', 'telefone_empresa', 'email_contato_empresa',
            'rua_empresa', 'bairro_empresa', 'cidade_empresa', 'estado_empresa'
        ]
        labels = {
            'nome_empresa': 'Nome da Empresa',
            'cnpj_empresa': 'CNPJ da Empresa',
            'telefone_empresa': 'Contato',
            'email_contato_empresa': 'Email',
            'rua_empresa': 'Rua',
            'bairro_empresa': 'Bairro',
            'cidade_empresa': 'Cidade',
            'estado_empresa': 'Estado',
        }
        widgets = {
            'estado_empresa': forms.Select(choices=[
                ('', 'Selecione um estado'),
                ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
                ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
                ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
                ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
                ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
                ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
                ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'),
            ]),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Tornar alguns campos opcionais, se necessário
        self.fields['cnpj_empresa'].required = False
        self.fields['email_contato_empresa'].required = False
        self.fields['telefone_empresa'].required = False
        # self.fields['bairro_empresa'].required = False
        # self.fields['email_contato_empresa'].required = False
        # self.fields['email_contato_empresa'].required = False

        # Placeholders para os campos do model
        self.fields['nome_empresa'].widget.attrs['placeholder'] = 'Ex: Clínica Pet Amor'
        self.fields['cnpj_empresa'].widget.attrs['placeholder'] = '00.000.000/0001-00'
        self.fields['telefone_empresa'].widget.attrs['placeholder'] = '(99) 99999-9999'
        self.fields['email_contato_empresa'].widget.attrs['placeholder'] = 'contato@empresa.com'
        self.fields['rua_empresa'].widget.attrs['placeholder'] = 'Rua das Flores, 123'
        self.fields['bairro_empresa'].widget.attrs['placeholder'] = 'Centro'
        self.fields['cidade_empresa'].widget.attrs['placeholder'] = 'São Paulo'

        # Campos adicionais do form
        self.fields['email_usuario'].widget.attrs['placeholder'] = 'seuemail@gmail.com'
        self.fields['api_key'].widget.attrs['placeholder'] = 'Chave da API Google'
        self.fields['remetente'].widget.attrs['placeholder'] = 'Ex: Recepção Clínica Pet <contato@gmail.com>'
        self.fields['whatsapp_nome'].widget.attrs['placeholder'] = 'Ex: Comercial Vet Pet'
        self.fields['whatsapp_numero'].widget.attrs['placeholder'] = '5582XXXXXXXXX'



    def save(self, commit=True):
        # Salvar CadastroEmpresa
        empresa = super().save(commit=commit)

        # Salvar EmailSMTPUsuario
        email_smtp = EmailSMTPUsuario(
            email_usuario=self.cleaned_data['email_usuario'],
            chave_api_secret_usuario=self.cleaned_data['api_key'],
            remetente_email_usuario=self.cleaned_data['remetente'],
            servidor_smtp_usuario="smtp.gmail.com",  # Padrão, pode ser alterado depois
            porta_smtp_usuario=587,
            usa_tls_usuario=True
        )
        if commit:
            email_smtp.save()

        # Salvar APIEvoUsuario
        api_evo = APIEvoUsuario(
            telefone_usuario_api=self.cleaned_data['whatsapp_numero'],
            nome_conexao=self.cleaned_data['whatsapp_nome'],
            ativo=True
        )
        if commit:
            api_evo.save()

        return empresa