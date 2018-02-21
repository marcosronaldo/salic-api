# coding=utf-8
from salic_api.models import Nomes, Agentes, Internet, Pais, UF, Municipios, Deslocamento

#
# Global constants
#
CPF = '1234'


def nomes_example(size=1):
    return [Nomes(idNome=i, idAgente=i, Descricao='Name %s' % i)
            for i in range(1, size + 1)]


def agentes_example(size=1):
    return [Agentes(idAgente=i, CNPJCPF=CPF)
            for i in range(1, size + 1)]


def internet_example(size=1):
    return [Internet(idInternet=i, idAgente=i, Descricao='email %s' % i)
            for i in range(1, size + 1)]


def pais_example(size=1):
    return [Pais(idPais=i, Descricao='Pais %s' % i)
            for i in range(1, size + 1)]


def uf_example(size=1):
    return [UF(iduf=i, Descricao="UF %s" % i)
            for i in range(1, size + 1)]


def municipio_example(size=1):
    return [Municipios(idMunicipioIBGE=i, Descricao="Municipio %s" % i)
            for i in range(1, size + 1)]


def deslocamento_example(size=1):
    return [Deslocamento(idDeslocamento=i, Qtde=i*2, idProjeto=i, idPaisOrigem=i,
                        idUFOrigem=i, idMunicipioOrigem=i, idPaisDestino=i,
                        idUFDestino=i, idMunicipioDestino=i)
            for i in range(1, size + 1)]
