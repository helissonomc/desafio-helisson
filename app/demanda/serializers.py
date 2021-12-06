from django.contrib.auth import get_user_model, authenticate
from django.db.models import fields
from rest_framework import serializers
from core.models import Demanda

class DemandaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Demanda
        fields = ('id', 'nome_peca', 'descricao_peca', 'endereco', 'info_contato', 'status_finalizacao')
        read_only_fields = ('id',)