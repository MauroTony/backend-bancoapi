from decimal import Decimal
from rest_framework import serializers
from django.db.models import Sum
from django.db.models.functions import Coalesce
from ..models import Cliente, Conta, Fatura, TipoTransacao, Movimentacao
from ..constants import CREDITO, DEBITO, DEPOSITO, PAGAMENTO_FATURA


class TransacaoSerializer(serializers.Serializer):
    conta = serializers.IntegerField()
    valor = serializers.DecimalField(max_digits=10, decimal_places=2)
    descricao = serializers.CharField()
    tipo_transacao = serializers.IntegerField()

    class Meta:
        fields = (
            "conta",
            "tipo_transacao",
            "valor",
            "descricao",
        )

    def validate(self, instancia):
        try:
            Cliente = Conta.objects.get(conta=instancia["conta"])
        except Conta.DoesNotExist:
            raise serializers.ValidationError({"error": "CONTA_INEXISTENTE"})
        try:
            TipoTransacao.objects.get(codigo_tipo=instancia["tipo_transacao"])
        except TipoTransacao.DoesNotExist:
            raise serializers.ValidationError({"error": "TIPO_TRANSACAO_INEXISTENTE"})

        if instancia["valor"] <= 0:
            raise serializers.ValidationError({"error": "VALOR_INVALIDO"})

        DepositoTotal = Movimentacao.objects.filter(
            conta=Cliente.conta, tipo_transacao=DEPOSITO
        ).aggregate(total=Coalesce(Sum("valor"), Decimal(0.0)))
        DebitoTotal = Movimentacao.objects.filter(
            conta=Cliente.conta, tipo_transacao__in=[DEBITO, PAGAMENTO_FATURA]
        ).aggregate(total=Coalesce(Sum("valor"), Decimal(0.0)))
        Saldo = DepositoTotal["total"] - DebitoTotal["total"]
        Cliente.saldo = Saldo
        Cliente.save()

        if instancia["tipo_transacao"] == DEBITO:
            if instancia["valor"] > Cliente.saldo:
                raise serializers.ValidationError({"error": "SALDO_INSUFICIENTE"})
        elif instancia["tipo_transacao"] == DEPOSITO:
            if instancia["valor"] < 0:
                raise serializers.ValidationError({"error": "VALOR_INVALIDO"})
        elif instancia["tipo_transacao"] == CREDITO:
            if Cliente.status_fatura == 3:
                raise serializers.ValidationError({"error": "FATURA_VENCIDA"})
            if Cliente.status_fatura == 1:
                raise serializers.ValidationError({"error": "FATURA_FECHADA"})
            fatura = Fatura.objects.filter(
                conta=Cliente.conta, status_pagamento=False
            ).first()
            gastos_fatura = Movimentacao.objects.filter(
                conta=Cliente.conta,
                data_movimentacao__gte=fatura.data_abertura,
                data_movimentacao__lte=fatura.data_vencimento,
                tipo_transacao=2,
            )
            gastos_fatura = gastos_fatura.aggregate(
                total=Coalesce(Sum("valor"), Decimal(0.0))
            )["total"]
            Cliente.credito_utilizado = gastos_fatura
            fatura.valor = gastos_fatura
            fatura.save()
            Cliente.save()
            if instancia["valor"] > Cliente.limite_credito - Cliente.credito_utilizado:
                raise serializers.ValidationError({"error": "CREDITO_INSUFICIENTE"})
        return instancia

    def create(self, instancia):
        Cliente = Conta.objects.get(conta=instancia["conta"])
        Movimentacao.objects.create(
            conta=Cliente.conta,
            descricao=instancia["descricao"],
            valor=instancia["valor"],
            tipo_transacao_id=instancia["tipo_transacao"],
        )
        if instancia["tipo_transacao"] == DEBITO:
            Cliente.saldo -= instancia["valor"]
            Cliente.save()
        elif instancia["tipo_transacao"] == DEPOSITO:
            Cliente.saldo += instancia["valor"]
            Cliente.save()
        elif instancia["tipo_transacao"] == CREDITO:
            fatura = Fatura.objects.filter(
                conta=Cliente.conta, status_pagamento=False
            ).first()
            Cliente.credito_utilizado = Cliente.credito_utilizado + instancia["valor"]
            Cliente.save()
            fatura.valor = fatura.valor + instancia["valor"]
            fatura.save()
        return instancia
