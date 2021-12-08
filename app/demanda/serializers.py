from rest_framework import serializers
from core.models import Demanda


class DemandaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Demanda
        fields = (
            'id',
            'nome_peca',
            'descricao_peca',
            'endereco',
            'info_contato',
            'status_finalizacao',
        )
        read_only_fields = ('id', )