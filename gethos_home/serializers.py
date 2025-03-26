# gethos_home/serializers.py
from rest_framework import serializers
from .models import Contato, Campanha
import re


class ContatoSerializer(serializers.ModelSerializer):



    class Meta:
        model = Contato
        fields = ['id', 'nome', 'telefone','status']  # Campos que estou expondo

        read_only_fields = ['id', 'data_criacao']

    def validate_telefone(self, value):
        
        telefone = re.sub(r'\D', '', value)
        if not re.match(r'^\d{10,11}$', telefone):
            raise serializers.ValidationError("Digite um telefone válido com DDD (10 ou 11 dígitos).")
        if not telefone.startswith('55'):
            telefone = '55' + telefone
        return telefone


class CampanhaSerializer(serializers.ModelSerializer):
    contatos = serializers.PrimaryKeyRelatedField(many=True, queryset=Contato.objects.all())

    class Meta:
        model = Campanha
        fields = ['id', 'nome', 'mensagem', 'contatos']