import numpy as np
import pandas as pd
from domain.models import SimulationParams


def projetar_producao(params: SimulationParams) -> pd.Series:
    meses = np.arange(1, 25)
    base = params.team.num_vendedores * params.producao_por_vendedor
    crescimento = (1 + params.taxa_crescimento) ** (meses - 1)
    return pd.Series(base * crescimento, index=meses, name="Producao")


def calcular_recebiveis_empresa(params: SimulationParams) -> pd.Series:
    producao = projetar_producao(params)
    comissao_bruta = producao * params.rules.comissao_empresa
    meses = np.arange(1, 25)
    fluxo_matriz = pd.DataFrame(0.0, index=meses, columns=meses)
    for venda_mes in meses:
        cb = comissao_bruta.loc[venda_mes]
        valor4 = cb * params.rules.pct_4m / 4
        valor10 = cb * params.rules.pct_10m * 0.5 / 3
        for i in range(4):
            mes_pag = venda_mes + i
            if mes_pag <= 24:
                fluxo_matriz.at[mes_pag, venda_mes] += valor4
        for i in range(3):
            mes_pag = venda_mes + i
            if mes_pag <= 24:
                fluxo_matriz.at[mes_pag, venda_mes] += valor10
    fluxo = fluxo_matriz.sum(axis=1)
    fluxo.name = "Recebiveis_Empresa"
    return fluxo