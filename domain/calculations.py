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
    Retorna um DataFrame com colunas:
    ['Mes', 'Custo_Fixo_Total', 'Comissao_Gerente', 'Comissao_Supervisor',
     'Comissao_Vendedor', 'TopUp_Vendedor'] e calcula:
    - Custo fixo total por cargo
    - Comissão de gerente, supervisor e vendedores com fracionamento
    - Top-up do vendedor quando comissão < piso
    """
    # Implementar lógica de distribuição
    # 1) Para cada mês, calcular produção e base de comissão
    # 2) Fracionar comissao de gerente, supervisor e vendedor conforme regras
    # 3) Aplicar piso mínimo ao vendedor e calcular top-up
    # 4) Somar custo fixo + pagamentos de comissão
    pass