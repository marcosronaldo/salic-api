# coding=utf-8

from datetime import datetime

from salic_api.models import Prorrogacao

def prorrogacao_example(size=1):
    return [Prorrogacao(
        idProrrogacao=i,
        Logon=i,
        DtPedido=datetime(2000, 1, 1),
        DtInicio=datetime(2000, 1, 1),
        DtFinal=datetime(2000, 3, 1),
        Observacao='Observacao',
        Atendimento='A',
        idPronac=20001234)
        for i in range(1,size+1)
    ]


