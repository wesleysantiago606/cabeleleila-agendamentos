from fastapi import FastAPI
from .base import Base, engine
from .rotas import servicos, agendamentos, adm

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cabeleleila - Sistema de Gerenciamento")

app.include_router(servicos.router)
app.include_router(agendamentos.router)
app.include_router(adm.router)