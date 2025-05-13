import streamlit as st
import plotly.express as px

def show():
    st.header("3. Resultados")
    result = st.session_state.get("result")
    if not result:
        st.warning("Simulação ainda não executada.")
        return
    meses = result.producao.index

    # Projeção de produção
    fig_prod = px.line(
        x=meses,
        y=result.producao,
        labels={"x": "Mês", "y": "Produção (R$)"},
        title="Projeção de Produção Mensal"
    )
    st.plotly_chart(fig_prod)

    # Fluxo de recebíveis
    fig_rec = px.bar(
        x=meses,
        y=result.recebiveis,
        labels={"x": "Mês", "y": "Recebíveis (R$)"},
        title="Fluxo de Recebíveis da Empresa"
    )
    st.plotly_chart(fig_rec)