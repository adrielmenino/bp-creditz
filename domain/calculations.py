import numpy as np
import pandas as pd
from domain.models import SimulationParams, TeamStructure, CommissionRules


def projetar_producao(params: SimulationParams) -> pd.Series:
    """
    Gera série mensal de produção bruta (R$) para 24 meses,
    aplicando crescimento composto.
    """
    meses = np.arange(1, 25)
    base = params.team.num_vendedores * params.producao_por_vendedor
    crescimento = (1 + params.taxa_crescimento) ** (meses - 1)
    return pd.Series(base * crescimento, index=meses, name="Producao")


def calcular_recebiveis_empresa(params: SimulationParams) -> pd.Series:
    """
    Calcula fluxo de recebíveis da empresa para 24 meses,
    considerando fracionamento pct_4m e pct_10m.
    """
    producao = projetar_producao(params)
    comissao_bruta = producao * params.rules.comissao_empresa
    meses = np.arange(1, 25)
    fluxo = pd.Series(0.0, index=meses, name="Recebiveis_Empresa")

    # Matriz para somar parcelas
    fluxo_matriz = pd.DataFrame(0.0, index=meses, columns=meses)
    for venda_mes in meses:
        cb = comissao_bruta.loc[venda_mes]
        # Fracionamento 4m: pagamento em 4 meses iguais
        parcela4 = cb * params.rules.pct_4m / 4
        # Fracionamento 10m: base reduzida 50%, paga em 3 meses
        parcela10 = cb * params.rules.pct_10m * 0.5 / 3
        # Distribui parcelas nos meses seguintes
        for i in range(4):
            mes_pag = venda_mes + i
            if mes_pag <= 24:
                fluxo_matriz.at[mes_pag, venda_mes] += parcela4
        for i in range(3):
            mes_pag = venda_mes + i
            if mes_pag <= 24:
                fluxo_matriz.at[mes_pag, venda_mes] += parcela10
    # Soma para obter fluxo mensal
    fluxo[:] = fluxo_matriz.sum(axis=1)
    return fluxo


def distribuir_comissoes(params: SimulationParams) -> pd.DataFrame:
    """
    Calcula custo fixo e distribui comissões de gerente, supervisor e vendedores,
    incluindo top-up de piso mínimo.
    Retorna DataFrame com índice 'Mes' e colunas:
      ['Custo_Fixo_Total', 'Comissao_Gerente', 'Comissao_Supervisor',
       'Comissao_Vendedor', 'TopUp_Vendedor', 'Total_Custo']
    """
    meses = np.arange(1, 25)
    producao = projetar_producao(params)

    # 1) Custo fixo total por mês (independente de vendas)
    custo_fixo_total = (
        params.team.num_vendedores   * params.team.custo_vendedor_fixo +
        params.team.num_supervisores * params.team.custo_supervisor_fixo +
        params.team.num_gerentes     * params.team.custo_gerente_fixo
    )

    # 2) Bases de comissão (antes de fracionar)
    comiss_gerente_bruta    = producao * params.rules.comissao_gerente
    if params.team.num_supervisores > 0:
        prod_por_sup        = producao / params.team.num_supervisores
    else:
        prod_por_sup        = pd.Series(0.0, index=meses)
    comiss_supervisor_bruta = prod_por_sup * params.rules.comissao_supervisor

    prod_por_vendedor      = producao / params.team.num_vendedores
    # total bruto de comissão vendedores (antes do piso)
    comiss_vendedor_bruta  = prod_por_vendedor * params.rules.comissao_vendedor * params.team.num_vendedores

    # 3) função interna de fracionamento 4m/10m
    def fracionar(serie_bruta: pd.Series) -> pd.Series:
        fluxo = pd.Series(0.0, index=meses)
        for t in meses:
            cb   = serie_bruta.loc[t]
            p4   = cb * params.rules.pct_4m / 4
            p10  = cb * params.rules.pct_10m * 0.5 / 3
            # parcelas 4 meses
            for i in range(4):
                m = t + i
                if m <= 24: fluxo.loc[m] += p4
            # parcelas 10 meses (3 meses)
            for i in range(3):
                m = t + i
                if m <= 24: fluxo.loc[m] += p10
        return fluxo

    flux_ger  = fracionar(comiss_gerente_bruta)
    flux_sup  = fracionar(comiss_supervisor_bruta)
    flux_vend = fracionar(comiss_vendedor_bruta)

    # 4) Top-up do piso para vendedores (pago no próprio mês de venda)
    comiss_vend_unit = prod_por_vendedor * params.rules.comissao_vendedor
    topup_unit       = (params.rules.salario_minimo_vendedor - comiss_vend_unit).clip(lower=0)
    topup_total      = topup_unit * params.team.num_vendedores

    # 5) Monta o DataFrame final
    df = pd.DataFrame({
        'Custo_Fixo_Total'   : custo_fixo_total,
        'Comissao_Gerente'   : flux_ger,
        'Comissao_Supervisor': flux_sup,
        'Comissao_Vendedor'  : flux_vend,
        'TopUp_Vendedor'     : topup_total
    }, index=meses)
    df['Total_Custo'] = df.sum(axis=1)
    df.index.name = 'Mes'
    return df