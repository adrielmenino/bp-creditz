import streamlit as st
from domain.models import SimulationParams, TeamStructure, CommissionRules
from app.service import SimulationService

def show():
    st.header("1. Parâmetros")
    with st.form("param_form"):
        # Base salary (salário fixo) is diferente do guarantee mínimo de comissão
        with st.expander("Salários Fixos da Equipe"):
            num_vendedores = st.number_input("Número de vendedores", min_value=1, value=1)
            salario_vendedor = st.number_input("Salário base por vendedor (R$)", min_value=0.0, value=5000.0)
            num_supervisores = st.number_input("Número de supervisores", min_value=0, value=1)
            salario_supervisor = st.number_input("Salário base por supervisor (R$)", min_value=0.0, value=8000.0)
            num_gerentes = st.number_input("Número de gerentes", min_value=0, value=1)
            salario_gerente = st.number_input("Salário base por gerente (R$)", min_value=0.0, value=10000.0)
        with st.expander("Regras de Comissão"):
            producao_por_vendedor = st.number_input("Produção média por vendedor (R$)", min_value=0.0, value=200000.0)
            taxa_crescimento = st.number_input("Crescimento mensal da produção (%)", min_value=0.0, value=0.0) / 100
            comissao_empresa = st.number_input("Comissão da empresa (%)", min_value=0.0, max_value=100.0, value=5.0) / 100
            pct_4m = st.number_input("Percentual 4 meses (%)", min_value=0.0, max_value=100.0, value=50.0) / 100
            pct_10m = 1 - pct_4m
            st.write(f"Percentual 10 meses: {pct_10m * 100:.1f}%")
            comissao_gerente = st.number_input("Comissão gerente (%)", min_value=0.0, max_value=100.0, value=1.0) / 100
            comissao_supervisor = st.number_input("Comissão supervisor (%)", min_value=0.0, max_value=100.0, value=2.0) / 100
            comissao_vendedor = st.number_input("Comissão vendedor (%)", min_value=0.0, max_value=100.0, value=3.0) / 100
            salario_minimo_vendedor = st.number_input("Piso de comissão vendedor (R$)", min_value=0.0, value=3000.0)
        submitted = st.form_submit_button("Simular")
    if submitted:
        team = TeamStructure(
            num_vendedores=int(num_vendedores),
            custo_vendedor_fixo=float(salario_vendedor),
            num_supervisores=int(num_supervisores),
            custo_supervisor_fixo=float(salario_supervisor),
            num_gerentes=int(num_gerentes),
            custo_gerente_fixo=float(salario_gerente)
        )
        rules = CommissionRules(
            comissao_empresa=comissao_empresa,
            pct_4m=pct_4m,
            pct_10m=pct_10m,
            comissao_gerente=comissao_gerente,
            comissao_supervisor=comissao_supervisor,
            comissao_vendedor=comissao_vendedor,
            salario_minimo_vendedor=salario_minimo_vendedor
        )
        params = SimulationParams(
            producao_por_vendedor=float(producao_por_vendedor),
            taxa_crescimento=float(taxa_crescimento),
            team=team,
            rules=rules
        )
        SimulationService.run(params)
        st.session_state["params"] = params
        st.success("Parâmetros validados e salvos!")