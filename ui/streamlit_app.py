import streamlit as st
from ui.pages import parametros, simulacao, resultados

def main():
    st.title("Simulador de equipes de consórcio.")

    tabs = st.tabs(["1. Parâmetros", "2. Simulação", "3. Resultados"])
    with tabs[0]:
        parametros.show()
    with tabs[1]:
        simulacao.show()
    with tabs[2]:
        resultados.show()