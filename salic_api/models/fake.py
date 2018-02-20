"""
Tables in this module emulate SQL procedures. We create those tables for
working with a local Sqlite db during testing.
"""

from sqlalchemy import Column, Integer, String, ForeignKey

from .base import Base


class Custos(Base):
    __tablename__ = 'Custos'

    idCustos = Column(Integer, primary_key=True)
    IdPRONAC = Column(String, ForeignKey("Projetos.IdPRONAC"))
    idInteressado = Column(String, ForeignKey("Interessado.CgcCpf"))
    valor_proposta = Column(Integer)
    valor_solicitado = Column(Integer)
    valor_aprovado = Column(Integer)
    valor_aprovado_convenio = Column(Integer)
    custo_projeto = Column(Integer)
    outras_fontes = Column(Integer)
