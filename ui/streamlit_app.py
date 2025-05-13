import streamlit as st
from ui.pages import parametros, simulacao, resultados

def main():
    st.sidebar.title("Simulador de Time Comercial")
    page = st.sidebar.radio("Navegar", ["Parâmetros", "Simulação", "Resultados"])
    if page == "Parâmetros":
        parametros.show()
    elif page == "Simulação":
        simulacao.show()
    else:
        resultados.show()