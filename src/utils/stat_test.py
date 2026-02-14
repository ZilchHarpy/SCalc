from parses import eh_erro_instrumental
import pandas as pd

tabela = pd.DataFrame({
    'Dados': ['a', 'b', 'c', 'd'],
    'I_err': [0.01, 0.02, 0.015, '0.018'],
    '1': [1, 2, 3, 4],
    '2': [4, 5, 6, 7],
    '3': [7, 8, 9, 10]
})

erros_instrumentais_list = []
dados_keys = []
dados_iteracoes = {}
dados = {}
erros_instrumentais = {}

for coluna in tabela.columns:
    if eh_erro_instrumental(coluna):
        erros_instrumentais_list = tabela[coluna].dropna().tolist()
    else:
        if 'dados' in str(coluna).lower():
            dados_keys = tabela[coluna].dropna().tolist()
        else:
            dados_iteracoes[coluna] = tabela[coluna].dropna().tolist()
        

for key in dados_keys:
    dados[key] = []
    erros_instrumentais[key] = []
    for coluna in dados_iteracoes:
        dados[key].append(dados_iteracoes[coluna][dados_keys.index(key)])
        erros_instrumentais[key].append(erros_instrumentais_list[dados_keys.index(key)])


print(dados)
print(erros_instrumentais)