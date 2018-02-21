# coding=utf-8
from salic_api.models import Nomes, Agentes, Internet, Pais, UF, Municipios, Deslocamento

#
# Global constants
#
CPF = '1234'


def nomes_example():
    return [Nomes(
        idNome=1,
        idAgente=1,
        Descricao='Name 1',
    )]


def agentes_example():
    return [Agentes(
        idAgente=1,
        CNPJCPF=CPF,
    )]


def internet_example():
    return [Internet(
        idInternet=1,
        idAgente=1,
        Descricao='email',
    )]


def pais_example():
    return [Pais(
        idPais=1,
        Descricao="Pais 1",
    )]


def uf_example():
    return [UF(
        iduf=1,
        Descricao="UF 1",
    )]


def municipio_example():
    return [Municipios(
        idMunicipioIBGE=1,
        Descricao="Municipio 1",
    )]


def deslocamento_example():
    return [Deslocamento(
        idDeslocamento=1,
        Qtde=2,
        idProjeto=1,
        idPaisOrigem=1,
        idUFOrigem=1,
        idMunicipioOrigem=1,
        idPaisDestino=1,
        idUFDestino=1,
        idMunicipioDestino=1,
    )]
