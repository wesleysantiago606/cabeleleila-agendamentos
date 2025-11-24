## Importações

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..base import get_db
from .. import modelos


router = APIRouter(prefix="/admin", tags=["Administração"])

## Dashboard do administrador do sistema
@router.get("/dashboard")
def painel_administrativo(db: Session = Depends(get_db)):
    """
    Retorna informações gerenciais básicas:
    - total de agendamentos
    - quantidade de agendamentos por serviço
    """

    total_agendamentos = db.query(modelos.Agendamento).count()

    uso_servicos = {}
    servicos = db.query(modelos.Servico).all()

    for servico in servicos:
        quantidade = db.query(modelos.Agendamento).filter(
            modelos.Agendamento.servico_id == servico.id
        ).count()

        uso_servicos[servico.nome] = quantidade

    return {
        "total_agendamentos": total_agendamentos,
        "servicos_mais_agendados": uso_servicos
    }