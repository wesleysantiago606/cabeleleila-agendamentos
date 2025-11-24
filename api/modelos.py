## Importações

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

## Tabela Serviço
class Servico(Base):
    __tablename__ = "servicos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    duracao_minutos = Column(Integer)
    preco = Column(Float)

## Tabela Agendamento
class Agendamento(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)
    cliente = Column(String)
    servico_id = Column(Integer, ForeignKey("servicos.id"))
    profissional = Column(String)
    data_hora = Column(DateTime)

    servico = relationship("Servico")