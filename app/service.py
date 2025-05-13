from types import SimpleNamespace
from domain.models import SimulationParams
from domain.calculations import (
    projetar_producao,
    calcular_recebiveis_empresa,
    distribuir_comissoes
)

class SimulationService:
    @staticmethod
    def run(params: SimulationParams) -> SimpleNamespace:
        # validação mínima
        if params.team.num_vendedores <= 0:
            raise ValueError("Número de vendedores deve ser maior que zero.")

        producao    = projetar_producao(params)
        recebiveis  = calcular_recebiveis_empresa(params)
        distribuicao = distribuir_comissoes(params)

        return SimpleNamespace(
            producao=producao,
            recebiveis=recebiveis,
            distribuicao=distribuicao
        )