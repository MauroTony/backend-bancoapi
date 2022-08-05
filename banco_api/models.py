from datetime import datetime
from http import client
from django.db import models
import pgtrigger


class Cliente(models.Model):
    cliente_id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    class Meta:
        db_table = "clientes"


class StatusFatura(models.Model):
    status_id = models.IntegerField(primary_key=True)
    descricao = models.CharField(max_length=20)

    class Meta:
        db_table = "status_fatura"


class Conta(models.Model):
    conta_id = models.AutoField(primary_key=True)
    conta = models.IntegerField(unique=True)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    limite_credito = models.DecimalField(max_digits=10, decimal_places=2, default=1000)
    credito_utilizado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vencimento_fatura = models.DateTimeField(null=True)
    status_fatura = models.ForeignKey(
        StatusFatura, on_delete=models.DO_NOTHING, null=True
    )
    cliente = models.OneToOneField(
        Cliente, on_delete=models.CASCADE, db_column="cliente_id"
    )
    credito_ativo = models.BooleanField(default=True)

    class Meta:
        db_table = "contas"


class Fatura(models.Model):
    fatura_id = models.AutoField(primary_key=True)
    conta = models.IntegerField()
    data_abertura = models.DateTimeField(default=datetime.now)
    data_vencimento = models.DateTimeField()
    data_pagamento = models.DateTimeField(null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    status_pagamento = models.BooleanField(default=False)

    class Meta:
        db_table = "faturas"


class TipoTransacao(models.Model):
    codigo_tipo = models.IntegerField(primary_key=True)
    descricao = models.CharField(max_length=100)


@pgtrigger.register(
    pgtrigger.Protect(name="protect_deletes", operation=pgtrigger.Delete)
)
class Movimentacao(models.Model):
    movimentacao_id = models.AutoField(primary_key=True)
    conta = models.IntegerField()
    data_movimentacao = models.DateTimeField(default=datetime.now)
    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_transacao = models.ForeignKey(
        TipoTransacao, on_delete=models.DO_NOTHING, db_column="codigo_tipo"
    )

    class Meta:
        db_table = "movimentacoes"
