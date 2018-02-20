# coding=utf-8
from salic_api.models import Custos

#
# Global constants
#
CPF = '1234'

def custos_example():
    return [Custos(
        idCustos=1,
        IdPRONAC='20001234',
        idInteressado=CPF,
        valor_proposta=1000,
        valor_solicitado=1000,
        valor_aprovado=1000,
        valor_aprovado_convenio=1000,
        custo_projeto=1000,
        outras_fontes=0,
    )]