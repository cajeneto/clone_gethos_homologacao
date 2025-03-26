from django import forms
from .models import ModeloMensagem
from .models import Campanha, FluxoAutomatizado, EtapaFluxo


class ModeloMensagemForm(forms.ModelForm):


    class Meta:
        model = ModeloMensagem
        fields = ['nome_modelo', 'tipo_mensagem', 'conteudo_mensagem']
        widgets = {
            'nome_modelo': forms.TextInput(attrs={'class': 'input-texto'}),
            'tipo_mensagem': forms.Select(attrs={'class': 'select-opcao'}),
        }




class CampanhaForm(forms.ModelForm):
    class Meta:
        model = Campanha
        fields = ['nome', 'status', 'mensagem']    



class FluxoAutomatizadoForm(forms.ModelForm):
     class Meta:
        model = FluxoAutomatizado
        fields = ['nome', 'descricao', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'input-text'}),
            'descricao': forms.Textarea(attrs={'class': 'input-area', 'rows': 3}),
            'ativo': forms.CheckboxInput(attrs={'class': 'input-checkbox'}),
        }


class EtapaFluxoForm(forms.ModelForm):
    class Meta:
        model = EtapaFluxo
        fields = ['ordem', 'canal', 'mensagem', 'delay_intervalo', 'intervalo_tipo']
        widgets = {
        'ordem': forms.NumberInput(attrs={'class': 'input-texto', 'min': 1}),
        'canal': forms.Select(attrs={'class': 'select-opcao'}),
        'mensagem': forms.Select(attrs={'class': 'select-opcao'}),
        'delay_intervalo': forms.NumberInput(attrs={'class': 'input-texto', 'min': 0}),
        'intervalo_tipo': forms.Select(attrs={'class': 'select-opcao'}),
        }