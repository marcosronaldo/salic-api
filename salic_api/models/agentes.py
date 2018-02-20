from sqlalchemy import Column, Integer, ForeignKey, String

from .base import Base


# This table actually describes city names!
class Nomes(Base):
    """
    Agentes.dbo.Nomes
    """
    __tablename__ = 'Nomes'

    idNome = Column(Integer, primary_key=True)
    idAgente = Column(Integer, ForeignKey('Agentes.idAgente'))
    Descricao = Column(String)


class Agentes(Base):
    """
    Agentes.dbo.Agentes
    """
    __tablename__ = 'Agentes'

    idAgente = Column(Integer, primary_key=True)
    CNPJCPF = Column(String)


class Internet(Base):
    """
    Agentes.dbo.Internet
    """
    __tablename__ = 'Internet'

    idInternet = Column(Integer, primary_key=True)
    idAgente = Column(Integer, ForeignKey('Agentes.idAgente'))
    Descricao = Column(String)


class Pais(Base):
    """
    Agentes.dbo.Pais
    """
    __tablename__ = 'Pais'

    idPais = Column(Integer, primary_key=True)
    Descricao = Column(String)


class UF(Base):
    """
    Agentes.dbo.uf
    """
    __tablename__ = 'uf'

    iduf = Column(Integer, primary_key=True)
    Descricao = Column(String)


class Municipios(Base):
    """
    Agentes.dbo.Municipios
    """
    __tablename__ = 'Municipios'

    idMunicipioIBGE = Column(Integer, primary_key=True)
    Descricao = Column(String)
