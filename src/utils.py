import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import re
import math

# Calcula a media, erro estatistico e erro total. Retorna uma tupla com esses parametros
def Calcular_Estatisticas(tabela):

    dados_brutos, erros_instr = Particionar(tabela)

    medias = {}
    erros_est = {}
    erros_instrumentais = {}
    erros_totais = {}

    tmp = defaultdict(list)
    aux = {}

    # Agrupa as listas por letra
    for chave, valores in dados_brutos.items():
        letras = re.match(r'([a-zA-Z]+)', chave)
        if letras:
            indice = letras.group(1)
            tmp[indice].append(valores)

    # Conta quantidade de listas por grupo (ex: y tem 3 listas: y1, y2, y3)
    for chave, listas in tmp.items():
        aux[chave] = len(listas)

    # Extrai erros instrumentais e mapeia para as keys corretas
    for chave_err, valores_err in erros_instrumentais.items():
        match = re.match(r'([a-zA-Z]+)err_instr', chave_err)
        if match:
            letra = match.group(1)
            erros_instrumentais[letra] = valores_err
    
    # Calcula a média dos elementos
    for chave, listas in tmp.items():
        medias[chave] = [float(sum(x)) / float(aux[chave]) for x in zip(*listas)]

    # Calcula o erro padrão da média (Standard Error of the Mean)
    for chave, listas in tmp.items():
        n = aux[chave]  # número de parâmetros (colunas)
        erros = []

        # Para cada posição (linha)
        for i, media_valor in enumerate(medias[chave]):

            # Coleta todos os valores dessa posição
            valores_posicao = [lista[i] for lista in listas]

            # Calcula a variância
            variancia = sum((valor - media_valor) ** 2 for valor in valores_posicao)

            if n > 1:
                erro_padrao = math.sqrt(variancia / (n * (n - 1)))
            else:
                erro_padrao = 0.0
            
            erros.append(erro_padrao)
            
        erros_est[chave] = erros
    

    # Calcula erro total: combinação do erro estatístico e erro instrumental
    # Erro total = sqrt(erro_estatístico^2 + erro_instrumental^2)
    for chave in medias.keys():
        if chave in erros_instrumentais:
            erros_totais_lista = []
            
            for i in range(len(medias[chave])):
                erro_stat = erros_est[chave][i]
                erro_inst = erros_instrumentais[chave][i]
                
                # Propagação de erros independentes
                erro_total = math.sqrt(erro_stat ** 2 + erro_inst ** 2)
                erros_totais_lista.append(erro_total)
            
            erros_totais[chave] = erros_totais_lista
        else:
            # Se não houver erro instrumental, usa apenas o erro estatístico
            erros_totais[chave] = erros_est[chave].copy()


    return medias, erros_est, erros_totais
# ---------------------------------------------------------------------------

# Particiona a tabela em dicionarios de dados e erros e os retorna
def Particionar(tabela):
#  Remover linhas e colunas vazias
    tabela = tabela.dropna(how='all', axis=0)
    tabela = tabela.dropna(how='all', axis=1)

    # Separa os erros dos dados da tabela
    erros_list = []
    dados_brutos_list = []

    for coluna in tabela.columns:
        if 'err_instr' in str(coluna).lower():
            erros_list.append(coluna)
        else:
            dados_brutos_list.append(coluna)

    # Cria dicionarios com as listas
    erros = {}
    dados_brutos = {}

    for coluna in dados_brutos_list:
        if 'medida' not in str(coluna).lower():
            dados_brutos[coluna] = tabela[coluna].dropna().tolist()

    for coluna in erros_list:
        erros[coluna] = tabela[coluna].dropna().tolist()

    return dados_brutos, erros
# ---------------------------------------------------------------------------

# Plota o grafico linearizado
def PlotarGrafico(pontos, erros_x, erros_y, n, ln_k):
    plt.style.use('_mpl-gallery')

    x, y = zip(*pontos)

    # Criar o gráfico com barras de erro
    fig, ax = plt.subplots()
    ax.errorbar(x, y, xerr=erros_x, yerr=erros_y, fmt='o', ecolor='red', capsize=5)

    # Adicionar a melhor reta
    x_fit = np.linspace(min(x), max(x), 100)
    y_fit = n * x_fit + ln_k
    ax.plot(x_fit, y_fit, color='blue', label='Melhor Reta')
    ax.legend()

    # Configurações do gráfico
    ax.set_title('Error Bar Plot with Best Fit Line')
    ax.set(xlim=(min(x) - 1, max(x) + 1), xticks=np.arange(min(x), max(x) + 2),
           ylim=(min(y) - 1, max(y) + 1), yticks=np.arange(min(y), max(y) + 2))

    plt.show()