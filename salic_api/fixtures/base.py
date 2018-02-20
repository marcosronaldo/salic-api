# coding=utf-8

from datetime import datetime

from salic_api.models import Prorrogacao


def prorrogacao_example():
    return [Prorrogacao(
        idProrrogacao=1,
        Logon=1,
        DtPedido=datetime(2000, 1, 1),
        DtInicio=datetime(2000, 1, 1),
        DtFinal=datetime(2000, 3, 1),
        Observacao='Observacao',
        Atendimento='A',
        idPronac=20001234,
    )]