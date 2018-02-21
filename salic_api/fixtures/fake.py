# coding=utf-8
from salic_api.models import Custos

#
# Global constants
#
CPF = '1234'


def custos_example(size=1):
    return [Custos(idCustos=i, IdPRONAC='20001234', idInteressado=CPF,
                    valor_proposta=1000*i, valor_solicitado=1000*i,
                    valor_aprovado=1000*i, valor_aprovado_convenio=1000*i,
                    custo_projeto=1000*i, outras_fontes=0)
            for i in range(1, size + 1)]
