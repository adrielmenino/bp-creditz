import streamlit as st
import plotly.express as px


def show():
    st.header("3. Resultados")
    result = st.session_state.get("result")
    if not result:
        st.warning("Simulação ainda não executada.")
        return

    # Dados principais
    df_prod = result.producao
    df_rec = result.recebiveis
    df_dist = result.distribuicao

    # 0) Métricas Agregadas
    net_flow = df_rec - df_dist['Total_Custo']
    cum_net = net_flow.cumsum()
    # Break-even: primeiro mês em que acumulado >= 0
    breakeven = int(cum_net[cum_net >= 0].index.min()) if (cum_net >= 0).any() else None
    total_receitas = df_rec.sum()
    total_custos = df_dist['Total_Custo'].sum()
    total_lucro = total_receitas - total_custos
    roi = total_lucro / total_custos if total_custos > 0 else None
    margem_media = ((df_rec - df_dist['Total_Custo']) / df_rec).mean()

    # Exibe KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Lucro Líquido Acumulado", f"R$ {total_lucro:,.0f}")
    col2.metric("ROI", f"{roi:.2%}" if roi is not None else "-")
    col3.metric("Margem Média", f"{margem_media:.2%}")
    col4.metric("Break-even", f"Mês {breakeven}" if breakeven else "Não alcançado")

    # 1) Projeção de Produção Mensal
    df1 = df_prod.reset_index()
    df1.columns = ["Mes", "Producao"]
    fig1 = px.line(
        df1, x="Mes", y="Producao",
        labels={"Mes": "Mês", "Producao": "Produção (R$)"},
        title="Projeção de Produção Mensal"
    )
    fig1.update_yaxes(tickformat=",.0f")
    st.plotly_chart(fig1, use_container_width=True)
    st.subheader("Tabela de Produção Mensal")
    st.dataframe(df1.style.format({"Producao": "R$ {:,.0f}"}), use_container_width=True)

    # 2) Fluxo de Recebíveis da Empresa
    df2 = df_rec.reset_index()
    df2.columns = ["Mes", "Recebiveis"]
    fig2 = px.bar(
        df2, x="Mes", y="Recebiveis",
        labels={"Mes": "Mês", "Recebiveis": "Recebíveis (R$)"},
        title="Fluxo de Recebíveis da Empresa"
    )
    fig2.update_yaxes(tickformat=",.0f")
    st.plotly_chart(fig2, use_container_width=True)
    st.subheader("Tabela de Recebíveis")
    st.dataframe(df2.style.format({"Recebiveis": "R$ {:,.0f}"}), use_container_width=True)

    # 3) Comissões Mensais e Top-up de Piso
    df3 = df_dist.reset_index()
    cols3 = ["Comissao_Gerente", "Comissao_Supervisor", "Comissao_Vendedor", "TopUp_Vendedor"]
    fig3 = px.line(
        df3, x="Mes", y=cols3,
        labels={"value": "Valor (R$)", "variable": "Categoria", "Mes": "Mês"},
        title="Comissões Mensais e Top-up de Piso"
    )
    fig3.update_yaxes(tickformat=",.0f")
    fig3.update_layout(legend_title_text="", legend_orientation="h", legend_y=-0.2)
    st.plotly_chart(fig3, use_container_width=True)
    st.subheader("Tabela de Comissões e Top-up")
    st.dataframe(df3[["Mes"] + cols3].style.format({c: "R$ {:,.0f}" for c in cols3}), use_container_width=True)

    # 4) Custo Total Mensal da Equipe
    df4 = df_dist.reset_index()
    fig4 = px.bar(
        df4, x="Mes", y="Total_Custo",
        labels={"Mes": "Mês", "Total_Custo": "Custo Total (R$)"},
        title="Custo Total Mensal da Equipe"
    )
    fig4.update_yaxes(tickformat=",.0f")
    st.plotly_chart(fig4, use_container_width=True)
    st.subheader("Tabela de Custo Total Mensal")
    st.dataframe(df4[["Mes", "Total_Custo"]].style.format({"Total_Custo": "R$ {:,.0f}"}), use_container_width=True)