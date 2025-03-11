from django import forms
from .models import Contato
<<<<<<< HEAD
from django.core.validators import RegexValidator
import re
from django.core.exceptions import ValidationError

# Validador que aceita apenas números e exige 10 ou 11 dígitos
telefone_validator = RegexValidator(r'^\d{10,11}$', 'Digite um número válido com DDD.')

class ContatoForm(forms.ModelForm):
    telefone = forms.CharField(validators=[telefone_validator])  # Validação de números

    class Meta:
        model = Contato
        fields = '__all__'

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone', '')

        # Remove todos os caracteres que não são números
        telefone = re.sub(r'\D', '', telefone)

        # Verifica se o telefone tem 10 ou 11 dígitos (com DDD)
        if not re.match(r'^\d{10,11}$', telefone):
            raise ValidationError("Digite um telefone válido com DDD.")

        # Adiciona automaticamente o código do Brasil (55) se ainda não tiver
        if not telefone.startswith('55'):
            telefone = '55' + telefone  # Adiciona 55 apenas se não tiver

        return telefone  # Retorna o telefone formatado com +55

class UploadExcelForm(forms.Form):
    arquivo_excel = forms.FileField(label='Selecione um arquivo Excel')




















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






=======

class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ['nome', 'email', 'telefone','empresa', 'status']



class UploadExcelForm(forms.Form):
    arquivo_excel = forms.FileField(label='Selecione um arquivo Excel')
>>>>>>> backup-local
