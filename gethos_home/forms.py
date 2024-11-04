from django import forms
from .models import Contato

class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ['nome', 'email', 'telefone','empresa', 'status']



class UploadExcelForm(forms.Form):
    arquivo_excel = forms.FileField(label='Selecione um arquivo Excel')
