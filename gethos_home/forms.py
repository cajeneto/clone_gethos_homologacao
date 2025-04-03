from django import forms
from .models import Contato, Usuario
from django.core.validators import RegexValidator
import re
from django.core.exceptions import ValidationError

# Validador que aceita apenas números e exige 10 ou 11 dígitos
telefone_validator = RegexValidator(r'^\d{10,11}$', 'Digite um número válido com DDD.')

class ContatoForm(forms.ModelForm):
    telefone = forms.CharField(
        validators=[telefone_validator],
        help_text="Digite o número com DDD (ex.: 82991326715). Se incluir +55, será ajustado automaticamente."
    )

    class Meta:
        model = Contato
        fields = '__all__'

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone', '')

        # Remove todos os caracteres que não são números (incluindo +)
        telefone = re.sub(r'\D', '', telefone)

        # Remove o código do país (55) se estiver presente
        if telefone.startswith('55') and len(telefone) > 11:
            telefone = telefone[2:]

        # Verifica se o telefone tem 10 ou 11 dígitos (com DDD)
        if not re.match(r'^\d{10,11}$', telefone):
            raise ValidationError("Digite um telefone válido com DDD (10 ou 11 dígitos). Ex.: 82991326715")

        # Adiciona o código do Brasil (55) para salvar no banco
        telefone = '55' + telefone

        return telefone

class UploadExcelForm(forms.Form):
    arquivo_excel = forms.FileField(label='Selecione um arquivo Excel')


class UsuarioEditForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'email', 'whatsapp']
        labels = {
            'first_name': 'Nome',
            'email': 'E-mail',
            'whatsapp': 'WhatsApp',
        }
        help_texts = {
            'whatsapp': 'Digite no formato +5511987654321',
        }


















# from django import forms
# from .models import Contato
# from django.core.validators import RegexValidator

# telefone_validator = RegexValidator(r'^\d{10,11}$', 'Digite um número válido.')



# class ContatoForm(forms.ModelForm):
#     telefone = forms.CharField(validators=[telefone_validator])
#     class Meta:
#         model = Contato
#         fields = '__all__' 



# class UploadExcelForm(forms.Form):
#     arquivo_excel = forms.FileField(label='Selecione um arquivo Excel')






