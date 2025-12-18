"""
Módulo de Estatística

Contém funções para cálculo de média, erro estatístico, erro instrumental
e erro total a partir de dados em DataFrame.
"""

import pandas as pd
import numpy as np
from collections import defaultdict
import re
import math


def Particionar(tabela: pd.DataFrame):
    """
    Particiona a tabela em dicionários de dados brutos e erros instrumentais.
    
    Args:
        tabela (pd.DataFrame): DataFrame com os dados completos
        
    Returns:
        tuple: (dados_brutos, erros) - dicionários com dados e erros
    """
    # Remover linhas e colunas vazias
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

    # Cria dicionários com as listas
    erros = {}
    dados_brutos = {}

    for coluna in dados_brutos_list:
        if 'medida' not in str(coluna).lower():
            dados_brutos[coluna] = tabela[coluna].dropna().tolist()

    for coluna in erros_list:
        erros[coluna] = tabela[coluna].dropna().tolist()

    return dados_brutos, erros


def Calcular_Estatisticas(tabela: pd.DataFrame):
    """
    Calcula a média, erro estatístico e erro total dos dados.
    
    Retorna uma tupla com três dicionários contendo as estatísticas calculadas
    para cada variável nos dados.
    
    Args:
        tabela (pd.DataFrame): DataFrame com os dados e erros instrumentais
        
    Returns:
        tuple: (medias, erros_est, erros_totais)
            - medias: dicionário com médias por variável
            - erros_est: dicionário com erros estatísticos
            - erros_totais: dicionário com erros totais (propagados)
    """

    # Particiona os dados brutos e erros instrumentais
    dados_brutos, erros_instr = Particionar(tabela)

    # Inicializa dicionários de resultados
    medias = {}
    erros_est = {}
    erros_instrumentais = {}
    erros_totais = {}
    aux = {}
    tmp = defaultdict(list)

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
    for chave_err, valores_err in erros_instr.items():
        match = re.match(r'([a-zA-Z]+)err_instr', chave_err)
        if match:
            letra = match.group(1)
            erros_instrumentais[letra] = valores_err

    # Calcula a média dos elementos
    for chave, listas in tmp.items():
        medias[chave] = [float(sum(x)) / float(aux[chave]) for x in zip(*listas)]

    # Calcula o erro padrão da média
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
