from sqlalchemy import Column, Date, DateTime, Integer, String, DATE, func, \
    VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# TODO: can we support the money type in the SQL Server?
Money = String
use_sqlite = True

if use_sqlite:
    DateTime = Date
    date_column = (lambda x: func.cast(x, VARCHAR))
else:
    date_column = (lambda x: func.cast(x, DATE))


# FIXME put right columns when given access to this table


# FIXME put right columns when given access to this table.
# for now using made up primary key
class Prorrogacao(Base):
    """
    ???.???.prorrogacao
    """
    __tablename__ = 'prorrogacao'

    idProrrogacao = Column(Integer, primary_key=True)
    Logon = Column(Integer)
    DtPedido = Column(DateTime)
    DtInicio = Column(DateTime)
    DtFinal = Column(DateTime)
    Observacao = Column(String)
    Atendimento = Column(String)
    idPronac = Column(Integer)
