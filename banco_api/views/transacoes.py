from random import seed
from random import randint
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView, status
from django.db import transaction

from ..models import Cliente, Conta, TipoTransacao, Movimentacao
from ..seriealizers import TransacaoSerializer


class transacaoAPIView(APIView):
    @transaction.atomic
    def post(self, request):
        data = request.data
        if "conta" not in data:
            return Response(
                {"error": "CONTA_OBRIGATORIO"}, status=status.HTTP_400_BAD_REQUEST
            )
        if "tipo_transacao" not in data:
            return Response(
                {"error": "TIPO_TRANSACAO_OBRIGATORIO"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if "valor" not in data:
            return Response(
                {"error": "VALOR_OBRIGATORIO"}, status=status.HTTP_400_BAD_REQUEST
            )

        transacao = TransacaoSerializer(data=data)
        transacao.is_valid(raise_exception=True)
        transacao.save()

        return Response()
