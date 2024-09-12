import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


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

def lcoe(fator_capacidade,capacidade, custo_planta, custo_fixo, custo_variavel, custo_combustivel, desconto, conversor=1, ano=1):
    energia_ano_ = energia_ano(capacidade, fator_capacidade)
    capex_ = capex(capacidade, custo_planta*conversor)
    opex_ = opex(custo_fixo*conversor, capacidade, custo_variavel, energia_ano_, custo_combustivel)
    vpl_opex_ = vpl_opex(opex_,desconto, ano)
    pv = vpl_energia(energia_ano_,desconto,ano)

    return (capex_ + vpl_opex_) / pv

def graph_trab_3(titulo, coal, gas):
    fator_capacidade = np.arange(0.1,1.3,0.1)
    
    dados = {
        'Fator Capacidade': fator_capacidade,
        'LCOE COAL': coal,
        'LCOE GAS': gas
    }
    
    df = pd.DataFrame(dados)
    
    plt.figure(figsize=(10,6))
    
    for fc in df.columns[1:]:
        plt.plot(df['Fator Capacidade'], df[fc], marker='o', label="LCOE COAL", color='b')
    for fc in df.columns[2:]:    
        plt.plot(df['Fator Capacidade'], df[fc], marker='s', label="LCOE GAS", color='r')
    
    plt.title(f'{titulo} X Fator Capacidade')
    plt.xlabel('Fator Capacidade')
    plt.ylabel('LCOE ($)')
    plt.legend()
    plt.grid(True)
    
    plt.show()

custo_planta_coal = 1100
custo_fixo_coal = 20
capacidade_coal = 400
custo_variavel_coal = 5
custo_combustivel_coal = 17
fator_capacidade_coal = 0.7

custo_planta_gas = 700
custo_fixo_gas = 9
capacidade_gas = 400
custo_variavel_gas = 3
custo_combustivel_gas = 40
fator_capacidade_gas = 0.7

desconto = 0.1
n = 25
ml = 1000

lcoe_coal = lcoe(fator_capacidade_coal,capacidade_coal, custo_planta_coal, custo_fixo_coal, custo_variavel_coal, custo_combustivel_coal, desconto, ml, n)

print(f"LCOE = {lcoe_coal}")

lcoe_gas = lcoe(fator_capacidade_gas,capacidade_gas, custo_planta_gas, custo_fixo_gas, custo_variavel_gas, custo_combustivel_gas, desconto, ml, n)

print(f"LCOE = {lcoe_gas}")

fator_capacidade = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1,1.2]

# COAL

lcoe_coal_ = []

for i in fator_capacidade:
    lcoe_aux = lcoe(i,capacidade_coal, custo_planta_coal, custo_fixo_coal, custo_variavel_coal, custo_combustivel_coal, desconto, ml, n)
    lcoe_coal_.append(lcoe_aux)

# GAS

lcoe_gas_ = []

for i in fator_capacidade:
    lcoe_aux = lcoe(i,capacidade_gas, custo_planta_gas, custo_fixo_gas, custo_variavel_gas, custo_combustivel_gas, desconto, ml, n)
    lcoe_gas_.append(lcoe_aux)

graph_trab_3("LCOE", lcoe_coal_, lcoe_gas_)

fator_capacidade = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1,1.2]

# COAL

lcoe_coal_ = []

for i in fator_capacidade:
    energia_ano_coal = energia_ano(capacidade_coal, i)
    capex_ = capex(capacidade_coal, custo_planta_coal*ml)
    opex_ = opex(custo_fixo_coal*ml, capacidade_coal, custo_variavel_coal, energia_ano_coal, custo_combustivel_coal)
    vplOpex_ = vpl_opex(opex_, desconto, n)
    somaCapexVplOpex = capex_ + vplOpex_
    lcoe_coal_.append(somaCapexVplOpex)

# GAS

lcoe_gas_ = []

for i in fator_capacidade:
    energia_ano_gas = energia_ano(capacidade_gas, i)
    capex_ = capex(capacidade_gas, custo_planta_gas*ml)
    opex_ = opex(custo_fixo_gas*ml, capacidade_gas, custo_variavel_gas, energia_ano_gas, custo_combustivel_gas)
    vplOpex_ = vpl_opex(opex_, desconto, n)
    somaCapexVplOpex = capex_ + vplOpex_
    lcoe_gas_.append(somaCapexVplOpex)

graph_trab_3("LCOE", lcoe_coal_, lcoe_gas_)