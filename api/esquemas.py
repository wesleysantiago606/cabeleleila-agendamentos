from pydantic import BaseModel, Field
from datetime import datetime, date

##  Serviços
class ServicoBase(BaseModel):
    nome: str
    duracao_minutos: int
    preco: float


class ServicoCreate(ServicoBase):
    pass


class Servico(ServicoBase):
    id: int

    class Config:
        orm_mode = True

class AgendamentoBase(BaseModel):
    cliente: str = Field(..., description="Nome do cliente")
    servico_id: int = Field(..., description="ID do serviço escolhido")
    profissional: str = Field(..., description="Nome do profissional")
    data_hora: datetime = Field(..., description="Data e hora do agendamento")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class AgendamentoCreate(AgendamentoBase):
    pass


class Agendamento(AgendamentoBase):
    id: int

    class Config:
        orm_mode = True

class SugestaoAgendamento(BaseModel):
    aviso: str
    agendamento_sugerido: bool
    cliente: str
    profissional: str
    servico_id: int
    data_hora_sugerida: date

class Reagendamento(BaseModel):
    nova_data_hora: datetime