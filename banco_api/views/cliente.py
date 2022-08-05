from datetime import datetime, timedelta
import email
from random import seed
from random import randint
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView, status
from django.db import transaction
from rest_framework.generics import ListAPIView

from banco_api.paginations.extrato import ExtratoPagination

from ..models import Cliente, Conta, TipoTransacao, Movimentacao, Fatura
from ..seriealizers import ContaSerializer, ExtratoSerializer


class ClienteCreateAPIView(APIView):
    @transaction.atomic
    def post(self, request):
        data = request.data
        if "nome" not in data:
            return Response(
                {"error": "NOME_OBRIGATORIO"}, status=status.HTTP_400_BAD_REQUEST
            )
        if "email" not in data:
            return Response(
                {"error": "EMAIL_OBRIGATORIO"}, status=status.HTTP_400_BAD_REQUEST
            )
        exist_email = Cliente.objects.filter(email=data["email"]).exists()
        if exist_email:
            return Response(
                {"error": "EMAIL_CADASTRADO"}, status=status.HTTP_400_BAD_REQUEST
            )
        cliente = Cliente.objects.create(nome=data["nome"], email=data["email"])
        seed(cliente.cliente_id)
        conta = Conta.objects.create(
            conta=randint(101, 1000000),
            cliente=cliente,
            limite_credito=1000,
            credito_utilizado=0,
            vencimento_fatura=datetime.now() + timedelta(minutes=20),
            status_fatura_id=2,
            credito_ativo=True,
            saldo=0,
        )
        Fatura.objects.create(
            conta=conta.conta,
            data_abertura=datetime.now(),
            data_vencimento=datetime.now() + timedelta(minutes=15),
        )
        return Response({"conta": conta.conta}, status=status.HTTP_201_CREATED)


class ClienteExtratoAPIView(ListAPIView):
    pagination_class = ExtratoPagination
    serializer_class = ExtratoSerializer

    def get_queryset(self):
        data = self.request.query_params
        if "conta" not in data:
            return ValidationError({"error": "CONTA_OBRIGATORIO"})
        conta = data["conta"]
        try:
            cliente = Conta.objects.get(conta=conta)
        except Conta.DoesNotExist:
            return ValidationError({"error": "CONTA_INEXISTENTE"})

        Extrato = (
            Movimentacao.objects.filter(conta=cliente.conta)
            .select_related("tipo_transacao")
            .order_by("-data_movimentacao")
        )

        if "tipo_transacao" in data:
            Extrato = Extrato.filter(tipo_transacao=data["tipo_transacao"])
        return Extrato


class VerificaClienteAPIView(APIView):
    def post(self, request):
        data = request.data
        if "conta" not in data:
            return Response(
                {"error": "CONTA_OBRIGATORIO"}, status=status.HTTP_400_BAD_REQUEST
            )
        conta = data["conta"]
        if not conta.isdigit():
            return Response(
                {"error": "CONTA_INEXISTENTE"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            cliente = Conta.objects.get(conta=conta)
        except Conta.DoesNotExist:
            return Response(
                {"error": "CONTA_INEXISTENTE"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(ContaSerializer(cliente).data)
