from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List

from ..base import get_db
from .. import modelos, esquemas
from pydantic import BaseModel

router = APIRouter(prefix="/agendamentos", tags=["Agendamentos"])

# Regra dos 2 dias
MIN_DIAS_ALTERACAO = 2


# --------------------
# MODELO P/ REAGENDAMENTO
# --------------------
class ReagendamentoBody(BaseModel):
    nova_data_hora: datetime


# --------------------
# SERIALIZAÇÃO
# --------------------
def _serialize_agendamento(ag):
    return {
        "id": ag.id,
        "cliente": ag.cliente,
        "servico_id": ag.servico_id,
        "profissional": ag.profissional,
        "data_hora": ag.data_hora.isoformat()
    }


# --------------------
# CRIAR AGENDAMENTO
# --------------------
@router.post("/")
def criar_agendamento(ag: esquemas.AgendamentoCreate, db: Session = Depends(get_db)):

    # Conflito do profissional no mesmo horário
    conflito = db.query(modelos.Agendamento).filter(
        modelos.Agendamento.profissional == ag.profissional,
        modelos.Agendamento.data_hora == ag.data_hora
    ).first()

    if conflito:
        raise HTTPException(
            status_code=400,
            detail="Este profissional já possui um agendamento neste horário."
        )

    # Sugestão de agendamento (mesma semana)
    target_dt: datetime = ag.data_hora
    ano, semana, _ = target_dt.isocalendar()

    lista_cliente: List[modelos.Agendamento] = db.query(modelos.Agendamento).filter(
        modelos.Agendamento.cliente == ag.cliente
    ).all()

    for existente in lista_cliente:
        if not isinstance(existente.data_hora, datetime):
            continue

        a, s, _ = existente.data_hora.isocalendar()
        if a == ano and s == semana:
            dia_sugerido = existente.data_hora.date()
            return {
                "aviso": f"Você já possui um agendamento nesta semana. Sugiro marcar também no dia {dia_sugerido}.",
                "agendamento_sugerido": True,
                "cliente": ag.cliente,
                "profissional": ag.profissional,
                "servico_id": ag.servico_id,
                "data_hora_sugerida": dia_sugerido.isoformat()
            }

    # Criação normal
    novo = modelos.Agendamento(**ag.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)

    return _serialize_agendamento(novo)


# --------------------
# LISTAR
# --------------------
@router.get("/", response_model=list[esquemas.Agendamento])
def listar_agendamentos(db: Session = Depends(get_db)):
    return db.query(modelos.Agendamento).all()


# --------------------
# ATUALIZAR
# --------------------
@router.put("/{agendamento_id}", response_model=esquemas.Agendamento)
def atualizar_agendamento(
    agendamento_id: int,
    dados: esquemas.AgendamentoCreate,
    db: Session = Depends(get_db)
):

    ag = db.query(modelos.Agendamento).filter(
        modelos.Agendamento.id == agendamento_id
    ).first()

    if not ag:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado.")

    agora = datetime.now()
    if (ag.data_hora - agora) < timedelta(days=MIN_DIAS_ALTERACAO):
        raise HTTPException(
            status_code=400,
            detail="Alterações só podem ser feitas com pelo menos 2 dias de antecedência."
        )

    for campo, valor in dados.model_dump().items():
        setattr(ag, campo, valor)

    db.commit()
    db.refresh(ag)
    return ag


# --------------------
# REAGENDAR
# --------------------
@router.put("/{agendamento_id}/reagendar", response_model=esquemas.Agendamento)
def reagendar_agendamento(
    agendamento_id: int,
    dados: ReagendamentoBody,
    db: Session = Depends(get_db)
):

    ag = db.query(modelos.Agendamento).filter(
        modelos.Agendamento.id == agendamento_id
    ).first()

    if not ag:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado.")

    agora = datetime.now()
    if (ag.data_hora - agora) < timedelta(days=MIN_DIAS_ALTERACAO):
        raise HTTPException(
            status_code=400,
            detail="Reagendamentos só podem ser feitos com pelo menos 2 dias de antecedência."
        )

    ag.data_hora = dados.nova_data_hora
    db.commit()
    db.refresh(ag)

    return ag
