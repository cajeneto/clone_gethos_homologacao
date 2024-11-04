from django import forms
from .models import ModeloMensagem
from .models import Campanha

class ModeloMensagemForm(forms.ModelForm):
    class Meta:
        model = ModeloMensagem
        fields = ['nome_modelo', 'tipo_mensagem', 'conteudo_mensagem']  # Campos que queremos exibir no formulário
        widgets = {
            'nome_modelo': forms.TextInput(attrs={'class': 'input-texto'}),
            'tipo_mensagem': forms.Select(attrs={'class': 'select-opcao'}),
            'conteudo_mensagem': forms.Textarea(attrs={'class': 'textarea-mensagem'}),
        }




class CampanhaForm(forms.ModelForm):
    class Meta:
        model = Campanha
        fields = ['nome', 'status', 'mensagem']    

