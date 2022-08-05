from rest_framework import serializers

from ..models import Cliente, Conta, TipoTransacao, Movimentacao


class ContaSerializer(serializers.ModelSerializer):
    nome_cliente = serializers.CharField(source="cliente.nome")

    class Meta:
        model = Conta
        fields = (
            "conta",
            "saldo",
            "limite_credito",
            "credito_utilizado",
            "vencimento_fatura",
            "nome_cliente",
        )


class ExtratoSerializer(serializers.ModelSerializer):
    transacao = serializers.CharField(source="tipo_transacao.descricao")

    class Meta:
        model = Movimentacao
        fields = ("data_movimentacao", "transacao", "descricao", "valor")
