from types import SimpleNamespace
from domain.models import SimulationParams
from domain.calculations import projetar_producao, calcular_recebiveis_empresa

class SimulationService:
    @staticmethod
    def run(params: SimulationParams) -> SimpleNamespace:
        # validações básicas
        if params.team.num_vendedores <= 0:
            raise ValueError("Número de vendedores deve ser maior que zero.")
        # Projeção de produção bruta
        serie_producao = projetar_producao(params)
        # Fluxo de recebíveis da empresa
        recebiveis = calcular_recebiveis_empresa(params)
        # TODO: distribuir comissões e calcular custos totais
        return SimpleNamespace(
            producao=serie_producao,
            recebiveis=recebiveis
        )