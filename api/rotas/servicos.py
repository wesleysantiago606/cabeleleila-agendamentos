## Importações

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..base import get_db
from .. import modelos, esquemas

## Rota da API
router = APIRouter(prefix="/servicos", tags=["Serviços"])

## Incluir novo serviço
@router.post("/", response_model=esquemas.Servico)
def criar_servico(servico: esquemas.ServicoCreate, db: Session = Depends(get_db)):
    novo_servico = modelos.Servico(**servico.dict())
    db.add(novo_servico)
    db.commit()
    db.refresh(novo_servico)
    return novo_servico

## Listar serviços
@router.get("/", response_model=list[esquemas.Servico])
def listar_servicos(db: Session = Depends(get_db)):
    return db.query(modelos.Servico).all()