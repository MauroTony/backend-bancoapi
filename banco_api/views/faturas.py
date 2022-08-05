from random import seed
from random import randint
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView, status
from django.db import transaction
from rest_framework.generics import ListAPIView
from ..models import Cliente, Conta, Fatura, TipoTransacao, Movimentacao
from ..seriealizers import FaturaVisualizacaoSerializer, FaturaPagamentoSerializer


class FaturaPagamentoAPIView(APIView):
    def post(self, request):
        data = request.data
        if "conta" not in data:
            return Response(
                {"error": "CONTA_OBRIGATORIO"}, status=status.HTTP_400_BAD_REQUEST
            )
        if "fatura_id" not in data:
            return Response(
                {"error": "FATURA_OBRIGATORIO"}, status=status.HTTP_400_BAD_REQUEST
            )

        fatura = Fatura.objects.filter(fatura_id=data["fatura_id"]).values()[0]

        pagamento = FaturaPagamentoSerializer(data=fatura)
        pagamento.is_valid(raise_exception=True)
        pagamento.save()
        return Response(
            {"success": "Fatura paga com sucesso"}, status=status.HTTP_200_OK
        )


class FaturaVisualizacaoAPIView(APIView):
    def post(self, request):
        data = request.data
        if "conta" not in data:
            return Response(
                {"error": "CONTA_OBRIGATORIO"}, status=status.HTTP_400_BAD_REQUEST
            )
        conta = data["conta"]
        try:
            cliente = Conta.objects.get(conta=conta)
        except Conta.DoesNotExist:
            return Response(
                {"error": "CONTA_INEXISTENTE"}, status=status.HTTP_400_BAD_REQUEST
            )

        fatura_atual = (
            Fatura.objects.filter(conta=cliente.conta)
            .order_by("-data_abertura")
            .first()
        )

        return Response(FaturaVisualizacaoSerializer(fatura_atual).data)
