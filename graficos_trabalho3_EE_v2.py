import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# Funções
def capex(capacidade, custo_planta):
    return capacidade * custo_planta

def energia_ano(capacidade, fator_capacidade):
    return capacidade * (365 * 24) * fator_capacidade

def opex(custo_fixo, capacidade, custo_variavel, energia_ano, custo_combustivel):
    cta = custo_fixo * capacidade
    cva = energia_ano * custo_variavel
    cca = energia_ano * custo_combustivel
    return cta + cva + cca

def vpl_opex(opex, desconto, ano):
    return sum(opex/(1 + (desconto**i)) for i in range(1, ano+1))

def vpl_energia(energia, desconto, ano):
    return sum(energia/(1 + (desconto**i)) for i in range(1,ano+1))

def lcoe(fator_capacidade, capacidade, custo_planta, custo_fixo, custo_variavel, custo_combustivel, desconto, conversor=1, ano=1):
    energia_ano_ = energia_ano(capacidade, fator_capacidade)
    capex_ = capex(capacidade, custo_planta*conversor)
    opex_ = opex(custo_fixo*conversor, capacidade, custo_variavel, energia_ano_, custo_combustivel)
    vpl_opex_ = vpl_opex(opex_,desconto, ano)
    pv = vpl_energia(energia_ano_,desconto,ano)

    return (capex_ + vpl_opex_) / pv

# Aplicação Dash
app = dash.Dash(__name__)

# Layout da interface
app.layout = html.Div([
    html.H1("Simulação de LCOE para COAL e GAS"),

    # Slider de entrada para fator de capacidade
    html.Div([
        html.Label('Fator Capacidade'),
        dcc.Slider(id='fator_slider', min=0.1, max=1.2, step=0.1, value=0.7),
        html.Div(id='slider_output', style={'margin-top': 20}),
    ], style={'width': '50%', 'display': 'inline-block'}),
    
    # Primeiro gráfico (LCOE)
    dcc.Graph(id='lcoe_graph'),

    # Segundo gráfico (Capex + VPL Opex)
    dcc.Graph(id='lcoe_soma_graph')
])

# Callback para atualizar os gráficos
@app.callback(
    [Output('lcoe_graph', 'figure'),
     Output('lcoe_soma_graph', 'figure'),
     Output('slider_output', 'children')],
    [Input('fator_slider', 'value')]
)
def update_lcoe_graph(fator_capacidade_value):
    # Parâmetros COAL
    custo_planta_coal = 1100
    custo_fixo_coal = 20
    capacidade_coal = 400
    custo_variavel_coal = 5
    custo_combustivel_coal = 17

    # Parâmetros GAS
    custo_planta_gas = 700
    custo_fixo_gas = 9
    capacidade_gas = 400
    custo_variavel_gas = 3
    custo_combustivel_gas = 40
    
    # Desconto e anos
    desconto = 0.1
    n = 25
    ml = 1000

    # Calculando LCOE para COAL e GAS
    lcoe_coal = []
    lcoe_gas = []
    soma_capex_vpl_opex_coal = []
    soma_capex_vpl_opex_gas = []

    fator_capacidade = np.arange(0.1, 1.3, 0.1)

    for i in fator_capacidade:
        # LCOE
        lcoe_coal.append(lcoe(i, capacidade_coal, custo_planta_coal, custo_fixo_coal, custo_variavel_coal, custo_combustivel_coal, desconto, ml, n))
        lcoe_gas.append(lcoe(i, capacidade_gas, custo_planta_gas, custo_fixo_gas, custo_variavel_gas, custo_combustivel_gas, desconto, ml, n))

        # Capex + VPL Opex
        energia_ano_coal = energia_ano(capacidade_coal, i)
        capex_coal = capex(capacidade_coal, custo_planta_coal * ml)
        opex_coal = opex(custo_fixo_coal * ml, capacidade_coal, custo_variavel_coal, energia_ano_coal, custo_combustivel_coal)
        vpl_opex_coal = vpl_opex(opex_coal, desconto, n)
        soma_capex_vpl_opex_coal.append(capex_coal + vpl_opex_coal)

        energia_ano_gas = energia_ano(capacidade_gas, i)
        capex_gas = capex(capacidade_gas, custo_planta_gas * ml)
        opex_gas = opex(custo_fixo_gas * ml, capacidade_gas, custo_variavel_gas, energia_ano_gas, custo_combustivel_gas)
        vpl_opex_gas = vpl_opex(opex_gas, desconto, n)
        soma_capex_vpl_opex_gas.append(capex_gas + vpl_opex_gas)

    # Gráfico 1: LCOE
    fig_lcoe = go.Figure()
    fig_lcoe.add_trace(go.Scatter(x=fator_capacidade, y=lcoe_coal, mode='lines+markers', name='LCOE COAL', line=dict(color='blue')))
    fig_lcoe.add_trace(go.Scatter(x=fator_capacidade, y=lcoe_gas, mode='lines+markers', name='LCOE GAS', line=dict(color='red')))
    fig_lcoe.update_layout(title='LCOE X Fator Capacidade', xaxis_title='Fator Capacidade', yaxis_title='LCOE ($)', hovermode='closest')

    # Gráfico 2: Capex + VPL Opex
    fig_soma_capex_vpl_opex = go.Figure()
    fig_soma_capex_vpl_opex.add_trace(go.Scatter(x=fator_capacidade, y=soma_capex_vpl_opex_coal, mode='lines+markers', name='Capex + VPL Opex COAL', line=dict(color='blue')))
    fig_soma_capex_vpl_opex.add_trace(go.Scatter(x=fator_capacidade, y=soma_capex_vpl_opex_gas, mode='lines+markers', name='Capex + VPL Opex GAS', line=dict(color='red')))
    fig_soma_capex_vpl_opex.update_layout(title='Capex + VPL Opex X Fator Capacidade', xaxis_title='Fator Capacidade', yaxis_title='Capex + VPL Opex ($)', hovermode='closest')

    return fig_lcoe, fig_soma_capex_vpl_opex, f'Fator Capacidade Selecionado: {fator_capacidade_value}'

# Executa o servidor
if __name__ == '__main__':
    app.run_server(debug=True)
