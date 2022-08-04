from http import client
from django.db import models
import pgtrigger
class Cliente(models.Model):
    cliente_id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    class Meta:
        db_table = 'clientes'


class Conta(models.Model):
    conta_id = models.AutoField(primary_key=True)
    conta = models.IntegerField(unique=True)
    saldo = models.DecimalField(max_digits=10, decimal_places=2)
    limite_credito = models.DecimalField(max_digits=10, decimal_places=2)
    credito_utilizado = models.DecimalField(max_digits=10, decimal_places=2)
    vencimento_fatura = models.DateField()
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, db_column='cliente_id')

    class Meta:
        db_table = 'contas'


class TipoTransacao(models.Model):
    codigo_tipo = models.IntegerField(primary_key=True)
    descricao = models.CharField(max_length=100)


@pgtrigger.register(
    pgtrigger.Protect(name='protect_deletes', operation=pgtrigger.Delete)
)
class Movimentacao(models.Model):
    movimentacao_id = models.AutoField(primary_key=True)
    conta = models.OneToOneField(Conta, on_delete=models.DO_NOTHING, db_column='conta')
    data_movimentacao = models.DateField()
    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_transacao = models.OneToOneField(TipoTransacao, on_delete=models.DO_NOTHING, db_column='codigo_tipo')

    class Meta:
        db_table = 'movimentacoes'