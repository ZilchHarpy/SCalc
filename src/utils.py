import numpy as np

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