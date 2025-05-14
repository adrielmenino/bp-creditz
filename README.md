# Simulador de Equipe de Consórcio

Este projeto é um **Simulador de Equipe de Consórcio**, desenvolvido em Python com Streamlit, Plotly e Pandas, que permite estimar:

* Projeção de produção mensal de vendas
* Fluxo de recebíveis da empresa (comissionamento parcelado 4m/10m)
* Distribuição de comissões (gerente, supervisor, vendedor) com piso mínimo
* Custos fixos da equipe e totais mensais
* Métricas financeiras agregadas (lucro acumulado, ROI, margem média, break‑even)

## Estrutura do Projeto

```
simulador_consorcio/
├── main.py                 # Ponto de entrada Streamlit
├── ui/                     # UI modularizada
│   ├── streamlit_app.py    # Layout com abas
│   └── pages/
│       ├── parametros.py   # Formulário de entrada
│       ├── simulacao.py    # Gatilho de execução
│       └── resultados.py   # Gráficos e tabelas de saída
├── app/                    # Camada de aplicação
│   └── service.py          # Orquestra chamadas de domínio
├── domain/                 # Camada de domínio e cálculos
│   ├── models.py           # Data classes e validações
│   └── calculations.py     # Funções de projeção e distribuição
├── requirements.txt        # Dependências Python
└── README.md               # Documentação do projeto
```

## Funcionalidades

1. **Entrada de parâmetros**

   * Salários fixos: vendedor, supervisor e gerente
   * Regras de comissão: produção média, crescimento, % comissionamento, mix 4m/10m
   * Piso mínimo de comissão para vendedores

2. **Simulação**

   * Projeção de produção composta para 24 meses
   * Cálculo de fluxo de recebíveis, fracionado em 4 e 10 meses
   * Distribuição de comissões e top‑up de piso
   * Cálculo de custo fixo, variável e total do time

3. **Resultados**

   * KPIs financeiros: lucro acumulado, ROI, margem média, break‑even
   * Gráficos interativos (Plotly) de todas as métricas
   * Tabelas com valores exatos formatados

## Requisitos

* **Python** >= 3.13.2
* **Bibliotecas**: especificadas em `requirements.txt`

## Instalação

```bash
# Clone o repositório
git clone https://github.com/adrielmenino/bp-creditz.git
cd bp-creditz

# Crie e ative um ambiente virtual
python -m venv .venv
# Windows
env\\Scripts\\activate
# macOS/Linux
source .venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

## Execução

```bash
# Inicia a interface Streamlit
streamlit run main.py
```

## Uso

1. Preencha os parâmetros de salário fixo e regras de comissão.
2. Clique em **Simulação** para rodar os cálculos.
3. Navegue para **Resultados** para visualizar gráficos, tabelas e KPIs.

## Próximos Passos

* Adição de cenários de sensibilidade (pessimista/base/otimista)
* Inserção de taxas de inadimplência e churn
* Exportação de relatórios em CSV/Excel/PDF
* Testes automatizados (pytest)
* Containerização e deploy (Docker, Streamlit Cloud)

---

*Desenvolvido por Adriel Menino*
