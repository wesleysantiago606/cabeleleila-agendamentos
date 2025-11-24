from datetime import datetime
from .base import SessionLocal
from . import modelos

def popular_banco_inicial():
    db = SessionLocal()

    ## Evitar duplicação
    if db.query(modelos.Servico).first():
        db.close()
        return

    ## Serviços iniciais
    servicos_iniciais = [
        modelos.Servico(nome="Corte Feminino", duracao_minutos=60, preco=80.0),
        modelos.Servico(nome="Corte Masculino", duracao_minutos=40, preco=50.0),
        modelos.Servico(nome="Escova", duracao_minutos=50, preco=70.0),
        modelos.Servico(nome="Tintura", duracao_minutos=120, preco=150.0),
        modelos.Servico(nome="Manicure", duracao_minutos=30, preco=35.0),
    ]

    db.add_all(servicos_iniciais)
    db.commit()

    ## Agendamentos iniciais 
    agendamentos_iniciais = [
        modelos.Agendamento(
            cliente="Renata",
            servico_id=1,
            profissional="Leila",
            data_hora=datetime.fromisoformat("2025-12-12T14:00:00")
        ),
        modelos.Agendamento(
            cliente="Wesley",
            servico_id=2,
            profissional="Suzana",
            data_hora=datetime.fromisoformat("2025-11-24T14:28:00")
        ),
    ]

    db.add_all(agendamentos_iniciais)
    db.commit()
    db.close()