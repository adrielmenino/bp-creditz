import streamlit as st
from app.service import SimulationService

def show():
    st.header("2. Simulação")
    params = st.session_state.get("params")
    if not params:
        st.warning("Defina os parâmetros antes de simular.")
        return
    if st.button("Rodar Simulação"):
        with st.spinner("Simulando..."):
            result = SimulationService.run(params)
        st.session_state["result"] = result
        st.success("Simulação concluída!")