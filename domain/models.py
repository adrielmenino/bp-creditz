from dataclasses import dataclass

@dataclass
class TeamStructure:
    """
    Representa o salário fixo (base) da equipe.
    Esse valor é sempre pago, independente de comissão.
    """
    num_vendedores: int
    custo_vendedor_fixo: float  # salário-base por vendedor
    num_supervisores: int
    custo_supervisor_fixo: float  # salário-base por supervisor
    num_gerentes: int
    custo_gerente_fixo: float  # salário-base por gerente

    def __post_init__(self):
        for field_name, value in self.__dict__.items():
            if isinstance(value, (int, float)) and value < 0:
                raise ValueError(f"{field_name} deve ser >= 0")


@dataclass
class CommissionRules:
    """
    Regras de comissão:
    - A empresa: comissão sobre produção, fracionada em 4m e 10m.
    - Gerente/Supervisor: recebem comissão adicional sobre produção, mas têm salário-base garantido.
    - Vendedor: piso de comissão garante um mínimo (pode exceder o salário-base).
    """
    comissao_empresa: float
    pct_4m: float
    pct_10m: float
    comissao_gerente: float
    comissao_supervisor: float
    comissao_vendedor: float
    salario_minimo_vendedor: float  # piso de comissão

    def __post_init__(self):
        if not 0 <= self.comissao_empresa <= 1:
            raise ValueError("comissao_empresa deve ser entre 0 e 1")
        if not 0 <= self.pct_4m <= 1:
            raise ValueError("pct_4m deve ser entre 0 e 1")
        if not 0 <= self.pct_10m <= 1:
            raise ValueError("pct_10m deve ser entre 0 e 1")
        if abs((self.pct_4m + self.pct_10m) - 1) > 1e-6:
            raise ValueError("pct_4m + pct_10m deve ser igual a 1")
        for name in ("comissao_gerente", "comissao_supervisor", "comissao_vendedor"):
            val = getattr(self, name)
            if not 0 <= val <= 1:
                raise ValueError(f"{name} deve ser entre 0 e 1")
        if self.salario_minimo_vendedor < 0:
            raise ValueError("salario_minimo_vendedor deve ser >= 0")


@dataclass
class SimulationParams:
    """
    Parâmetros de entrada para a simulação:
    - producao_por_vendedor: produção média mensal por vendedor (R$)
    - taxa_crescimento: crescimento composto mensal da produção (0–1)
    - team: estrutura de equipe com salários fixos
    - rules: regras de comissão e fracionamento
    """
    producao_por_vendedor: float
    taxa_crescimento: float
    team: TeamStructure
    rules: CommissionRules

    def __post_init__(self):
        if self.producao_por_vendedor < 0:
            raise ValueError("producao_por_vendedor deve ser >= 0")
        if self.taxa_crescimento < 0:
            raise ValueError("taxa_crescimento deve ser >= 0")
