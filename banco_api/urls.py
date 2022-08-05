from django.urls import path, include
from .views import (
    ClienteCreateAPIView,
    transacaoAPIView,
    VerificaClienteAPIView,
    ClienteExtratoAPIView,
    FaturaVisualizacaoAPIView,
    FaturaPagamentoAPIView,
)

urlpatterns = [
    path("cliente", ClienteCreateAPIView.as_view()),
    path("verifica_cliente", VerificaClienteAPIView.as_view()),
    path("transacao", transacaoAPIView.as_view()),
    path("extrato", ClienteExtratoAPIView.as_view()),
    path("visualizar_fatura", FaturaVisualizacaoAPIView.as_view()),
    path("pagamento_fatura", FaturaPagamentoAPIView.as_view()),
]
