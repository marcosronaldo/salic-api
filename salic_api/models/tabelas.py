from sqlalchemy import Column, Integer, String

from .base import Base


class Usuarios(Base):
    """
    Tabela que armazena dados do usuário.

    (TABELAS.dbo.Usuarios)
    """
    __tablename__ = 'Usuarios'

    usu_codigo = Column(Integer, primary_key=True)
    usu_nome = Column(String)
