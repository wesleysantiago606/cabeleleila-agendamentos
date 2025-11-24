# 💇 Sistema de Agendamentos – Cabeleleila Leila

Aplicação desenvolvida para atender aos requisitos do estabelecimento **Cabeleleila Leila**.  
A aplicação foi construída utilizando **Python**, com **FastAPI** no backend, **SQLite** como banco de dados e **Streamlit** para interface visual.

---

## Requisitos Funcionais

### Cadastro e exibição dos serviços contratados
- Descrição do serviço  
- Duração  
- Preço

### Agendamento de serviços
- Escolha de profissional  
- Seleção de serviço  
- Data e hora  
- Regra de conflito: **A aplicação não permite agendamento no mesmo horário para o mesmo profissional**

### Alteração de agendamentos
- Permitida somente com antecedência de **no mínimo 2 dias**

### Listagem de agendamentos  
- Exibição completa dos agendamentos cadastrados

### Dashboard administrativo
- Total de agendamentos  
- Estatísticas por tipo de serviço  

---

### Arquitetura implantada

cabeleleila leila - dsin/
│
├── api/
│ ├── main.py
│ ├── base.py
│ ├── modelos.py
│ ├── esquemas.py
│ └── rotas/
│ ├── servicos.py
│ ├── apontamentos.py
│ └── adm.py
│
├── interface/
│ └── app.py
│
├── requerimentos.txt
└── README.md

---

### Tecnologias

- **Python 3.10+**
- **FastAPI** (backend)
- **SQLite** (banco de dados)
- **SQLAlchemy** (ORM)
- **Streamlit** (interface)
- **Uvicorn** (servidor ASGI)