import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from dateutil import parser
from api.cadastro import popular_banco_inicial



popular_banco_inicial()

API = "http://localhost:8000"

st.set_page_config(page_title="Cabeleleila - Agendamentos", layout="wide")
st.title("Sistema de Agendamentos - Cabeleleila Leila")

menu = st.sidebar.selectbox("Menu", ["Agendar", "Listar Agendamentos", "Reagendar", "Dashboard"])

def safe_json(r):
    """Tenta extrair JSON da response; se falhar, retorna None."""
    try:
        return r.json()
    except Exception:
        return None

def fetch_servicos():
    r = requests.get(f"{API}/servicos/")
    return safe_json(r) or []

def fetch_agendamentos():
    r = requests.get(f"{API}/agendamentos/")
    return safe_json(r) or []

def pretty_date_iso(iso):
    try:
        dt = parser.isoparse(iso)
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return str(iso)


if menu == "Agendar":
    st.header("Novo Agendamento")

 
    col1, col2 = st.columns([2, 1])

    with col1:
        cliente = st.text_input("Nome do Cliente", key="cliente_input")
        profissional = st.text_input("Profissional", key="profissional_input")

    with col2:
        servicos = fetch_servicos()
        if servicos:
            servico_escolhido = st.selectbox("Serviço", servicos, format_func=lambda x: x["nome"], key="servico_select")
        else:
            servico_escolhido = None
            st.info("Nenhum serviço cadastrado. Rode o script de populacao ou cadastre serviços via API.")

   
    with st.form("form_agendar"):
        data = st.date_input("Data", key="date_input")
        hora = st.time_input("Hora", key="time_input")
        submit = st.form_submit_button("Agendar")

    if submit:
        if not cliente or not profissional or not servico_escolhido:
            st.warning("Preencha cliente, profissional e selecione um serviço.")
        else:
            data_hora = datetime.combine(data, hora).isoformat()
            payload = {
                "cliente": cliente,
                "profissional": profissional,
                "servico_id": servico_escolhido["id"],
                "data_hora": data_hora,
            }

            r = requests.post(f"{API}/agendamentos/", json=payload)
            content = safe_json(r)

            if content and content.get("agendamento_sugerido"):

                aviso = content.get("aviso", "Foi encontrada uma sugestão de data.")
                sugerida_iso = content.get("data_hora_sugerida")

                st.info(aviso)
                col_yes, col_no = st.columns([1, 1])
                with col_yes:
                    if st.button("Aceitar sugestão", key=f"aceitar_sug_{cliente}_{sugerida_iso}"):

                        payload_sug = {
                            "cliente": cliente,
                            "profissional": profissional,
                            "servico_id": servico_escolhido["id"],
                            "data_hora": sugerida_iso
                        }
                        r2 = requests.post(f"{API}/agendamentos/", json=payload_sug)
                        content2 = safe_json(r2)
                        if r2.status_code in (200, 201):
                            st.success("Agendamento criado com a data sugerida: " + pretty_date_iso(sugerida_iso))
                        else:

                            if content2 and content2.get("detail"):
                                st.error(content2.get("detail"))
                            else:
                                st.error(f"Erro ao criar agendamento (status {r2.status_code})")
                with col_no:
                    if st.button("Recusar sugestão", key=f"recusar_sug_{cliente}_{sugerida_iso}"):
                        st.info("Sugestão recusada. Você pode ajustar a data/hora e tentar novamente.")

 
            elif r.status_code in (200, 201):

                st.success("Agendamento realizado com sucesso!")
            else:

                if content and content.get("detail"):
                    st.error(content.get("detail"))
                else:
                    st.error(f"Erro inesperado (status {r.status_code}). Veja o console para detalhes.")


elif menu == "Listar Agendamentos":
    st.header("Todos os Agendamentos")

    dados = fetch_agendamentos()

    if not dados:
        st.info("Nenhum agendamento encontrado.")
    else:

        df = pd.DataFrame(dados)


        if "data_hora" in df.columns:
            df["data_hora"] = df["data_hora"].apply(lambda v: pretty_date_iso(v) if pd.notna(v) else v)

        df_display = df.rename(columns={
            "cliente": "Cliente",
            "servico_id": "Serviço (ID)",
            "profissional": "Profissional",
            "data_hora": "Data e Hora",
            "id": "Código"
        })

        st.table(df_display)


elif menu == "Reagendar":
    st.header("Alterar / Reagendar Agendamento")

    agendamentos = fetch_agendamentos()
    if not agendamentos:
        st.info("Nenhum agendamento para alterar.")
    else:

        options = [f"{a['id']} - {a['cliente']} ({pretty_date_iso(a.get('data_hora'))})" for a in agendamentos]
        sel = st.selectbox("Selecione o agendamento", options, key="select_reagendar")
        idx = options.index(sel)
        ag_sel = agendamentos[idx]

        st.subheader("Dados atuais")
        st.write(f"Cliente: **{ag_sel['cliente']}**")
        st.write(f"Profissional: **{ag_sel['profissional']}**")
        st.write(f"Data atual: **{pretty_date_iso(ag_sel.get('data_hora'))}**")
        st.write(f"Serviço (ID): **{ag_sel['servico_id']}**")

        st.markdown("---")
        st.subheader("Nova data / hora")

        nova_data = st.date_input("Nova Data", key="reag_date")
        nova_hora = st.time_input("Nova Hora", key="reag_time")
        nova_dt = datetime.combine(nova_data, nova_hora).isoformat()

        if st.button("Reagendar", key=f"btn_reag_{ag_sel['id']}"):

            payload = {"nova_data_hora": nova_dt}
            r = requests.put(f"{API}/agendamentos/{ag_sel['id']}/reagendar", json=payload)
            content = safe_json(r)
            if r.status_code in (200, 201):
                st.success("Agendamento reagendado para: " + pretty_date_iso(nova_dt))
            else:
                if content and content.get("detail"):
                    st.error(content.get("detail"))
                else:
                    st.error(f"Erro ao reagendar (status {r.status_code}).")


elif menu == "Dashboard":
    st.header("Painel Administrativo")

    dados = requests.get(f"{API}/admin/dashboard").json()

 
    total = dados.get("total_agendamentos", 0)
    st.metric("Total de Agendamentos", total)

    servicos_dict = dados.get("servicos_mais_agendados", {})
    if servicos_dict:
   
        df_serv = pd.DataFrame(list(servicos_dict.items()), columns=["Serviço", "Quantidade"])
        st.subheader("Serviços mais agendados")
        st.table(df_serv)


        chart = df_serv.set_index("Serviço")
        st.bar_chart(chart)
    else:
        st.info("Nenhum dado de serviços disponível no dashboard.")
