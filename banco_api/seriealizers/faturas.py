import datetime
from decimal import Decimal
from rest_framework import serializers
from django.db.models import Sum
from django.db.models.functions import Coalesce
from ..models import Cliente, Conta, Fatura, TipoTransacao, Movimentacao
from ..constants import CREDITO, DEBITO, DEPOSITO


class FaturaVisualizacaoSerializer(serializers.ModelSerializer):
    desc_fatura = serializers.SerializerMethodField()

    class Meta:
        model = Fatura
        fields = (
            "fatura_id",
            "data_abertura",
            "data_vencimento",
            "valor",
            "status_pagamento",
            "desc_fatura",
        )

    def get_desc_fatura(self, instancia):
        desc = (
            Conta.objects.filter(conta=instancia.conta).first().status_fatura.descricao
        )
        return desc


class FaturaPagamentoSerializer(serializers.Serializer):
    fatura_id = serializers.IntegerField()
    conta = serializers.IntegerField()
    valor = serializers.DecimalField(max_digits=10, decimal_places=2)
    status_pagamento = serializers.BooleanField()
    data_vencimento = serializers.DateTimeField()

    class Meta:
        fields = (
            "fatura_id",
            "conta",
            "data_abertura",
            "data_vencimento",
            "valor",
            "status_pagamento",
        )

    def validate(self, instancia):
        print("instancia: ", instancia["status_pagamento"])

        if instancia["status_pagamento"] == True:
            raise serializers.ValidationError({"error": "FATURA_PAGA"})
        conta = Conta.objects.filter(conta=instancia["conta"]).first()
        if conta.status_fatura.status_id == 2:
            raise serializers.ValidationError({"error": "FATURA_ABERTA"})
        if instancia["valor"] == 0:
            raise serializers.ValidationError({"error": "FATURA_ZERADA"})
        if conta.saldo < instancia["valor"]:
            raise serializers.ValidationError({"error": "SALDO_INSUFICIENTE"})
        return instancia

    def create(self, instancia):
        conta = Conta.objects.filter(conta=instancia["conta"]).first()
        Movimentacao.objects.create(
            conta=conta.conta,
            descricao="Pagamento de fatura",
            valor=instancia["valor"],
            tipo_transacao_id=4,
        )
        fatura = Fatura.objects.filter(fatura_id=instancia["fatura_id"]).first()
        fatura.status_pagamento = True
        fatura.data_pagamento = datetime.datetime.now()
        fatura.save()
        conta.saldo -= instancia["valor"]
        conta.credito_utilizado = Decimal(0)
        conta.status_fatura_id = 2
        conta.vencimento_fatura = datetime.datetime.now() + datetime.timedelta(
            minutes=20
        )
        conta.save()
        Fatura.objects.create(
            conta=instancia["conta"],
            data_abertura=datetime.datetime.now(),
            data_vencimento=datetime.datetime.now() + datetime.timedelta(minutes=15),
        )
        return instancia
