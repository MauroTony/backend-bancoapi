"""
from django_q.models import Schedule

Schedule.objects.create(func="banco_api.schedules.faturas", minutes=1, repeats=-1)
"""
import datetime
from decimal import Decimal
from .models import Conta, TipoTransacao, Movimentacao, Fatura, StatusFatura
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.db import transaction


@transaction.atomic
def faturas():
    print("Verificando Faturamentos")
    clientes = Conta.objects.filter(credito_ativo=True)
    clientes_aberto = clientes.filter(status_fatura_id=2)
    clientes_fechados = clientes.filter(status_fatura_id=1)
    for cliente in clientes_aberto:
        fatura = (
            Fatura.objects.filter(conta=cliente.conta)
            .order_by("-data_abertura")
            .first()
        )
        if fatura.data_vencimento < datetime.datetime.now():
            cliente.status_fatura_id = 1
            cliente.save()

            movimentacoes = Movimentacao.objects.filter(
                conta=cliente.conta,
                data_movimentacao__gte=fatura.data_abertura,
                data_movimentacao__lte=fatura.data_vencimento,
                tipo_transacao=2,
            )
            gastos = movimentacoes.aggregate(total=Coalesce(Sum("valor"), Decimal(0.0)))
            fatura.valor = gastos["total"]
            fatura.save()
            if fatura.valor == 0:
                fatura.status_pagamento = True
                fatura.data_pagamento = datetime.datetime.now()
                cliente.status_fatura_id = 2
                cliente.vencimento_fatura = (
                    datetime.datetime.now() + datetime.timedelta(minutes=20)
                )
                fatura.save()
                cliente.save()
                Fatura.objects.create(
                    conta=cliente.conta,
                    data_abertura=datetime.datetime.now(),
                    data_vencimento=datetime.datetime.now()
                    + datetime.timedelta(minutes=15),
                )
    for cliente in clientes_fechados:
        fatura = (
            Fatura.objects.filter(conta=cliente.conta, status_pagamento=False)
            .order_by("-data_abertura")
            .first()
        )
        if cliente.vencimento_fatura < datetime.datetime.now():
            cliente.status_fatura_id = 3
            cliente.credito_ativo = False
            cliente.save()
