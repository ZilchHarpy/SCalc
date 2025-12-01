import numpy as np
import matplotlib.pyplot as plt

# Calculo da média de uma lista de números
def calcular_media(lista):
    for i in range(len(lista)):
        lista[i] = float(lista[i])
    return sum(lista) / len(lista)

# Calculo do desvio padrão de uma lista de números
def calcular_desvio_padrao(lista):
    media = calcular_media(lista)
    n = len(lista)
    variancia = sum((x - media) ** 2 for x in lista) / (n-1)
    return np.sqrt(variancia)

# Calculo do erro estatístico da média
def calcular_erro_estatistico(lista):
    desvio_padrao = calcular_desvio_padrao(lista)
    n = len(lista)
    return desvio_padrao / np.sqrt(n)

# Calculo do erro total combinando erro estatístico e erro sistemático de uma lista de números
def calcular_erro_total(lista, erro_sistematico):
    erro_estatistico = calcular_erro_estatistico(lista)
    return np.sqrt(erro_estatistico**2 + erro_sistematico**2)

# Linearização logarítmica dos dados
def LinLog(t, y):
    '''
    Realiza a linearização logarítmica dos dados fornecidos de uma equação
    do tipo y = kt^n.
    Parâmetros:
    t : lista de valores t
    y : lista de valores y
    Retorna:
    t_log : lista de valores log(t)
    y_log : lista de valores log(y)
    n: coeficiente angular da regressão linear dos dados linearizados
    ln(k) : coeficiente linear da regressão linear dos dados linearizados

    '''

    t_log = [np.log(valor) for valor in t]
    y_log = [np.log(valor) for valor in y]
    n, ln_k = np.polyfit(t_log, y_log, 1)
    return t_log, y_log, n, ln_k

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

# Conta a quantidade de dados diferentes e retorna em uma lista seguindo a transformação de exemplo:
# [y1,y2,y3,x1,x2,w1,w2] --> [1,2,3,1,2,1,2] --> [3,2,2]
def contar_dados(data):
    # data = [y1,y2,y3,x1,x2,w1,w2]

    lista = {}

    # data --> lista = [1,2,3,1,2,1,2]
    for column in data.columns:
        lista[column] = data[column].dropna().astype(float).tolist()

    numeros = []

    # lista --> numeros = [3,2,2]
    for chave in lista.keys():
        numero = ''.join(filter(str.isdigit, chave))
        numeros.append(int(numero))
    
    cnt_num = []
    pos = 0
    i = 0
    while pos < len(numeros)-1:
        if(numeros[i] < numeros[i+1]):
            numeros.pop(i)
        else:
            pos += 1
        i = pos

    return numeros

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