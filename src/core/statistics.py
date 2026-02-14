"""
Módulo de Estatística

Contém funções para cálculo de média, erro estatístico, erro instrumental
e erro total a partir de dados em DataFrame.
"""

import logging
import pandas as pd
import numpy as np
from collections import defaultdict
import re
import math
from src.utils.parses import eh_erro_instrumental
from src.core.exceptions import (
    DadosInvalidosException,
    DadosInsuficientesException,
    ColunasInvalidasException
)

# Configura o logger
logger = logging.getLogger(__name__)

def particionar(tabela: pd.DataFrame):
    """
    Particiona a tabela em dicionários de dados brutos e erros instrumentais.
    
    Args:
        tabela (pd.DataFrame): DataFrame com os dados completos
        
    Returns:
        tuple: (dados, erros_instrumentais) - dicionários com dados e erros instrumentais]
    
    Examples:
        >>> tabela = pd.DataFrame({
        ...     'Dados': ['a', 'b', 'c', 'd'],
        ...     'I_err': [0.01, 0.02, 0.015, 0.01],
        ...     '1': [1, 2, 3],
        ...     '2': [4, 5, 6],
        ...     '3': [7, 8, 9]
        ... })
        >>> dados, erros_instrumentais = particionar(tabela)
        >>> dados
        {'a': [1, 4, 7], 'b': [2, 5, 8], 'c': [3, 6, 9]}
        >>> erros_instrumentais
        {'a': 0.01, 'b': 0.02, 'c': 0.015, 'd': 0.01}
    """
    # VALIDAÇÃO 1: DataFrame não pode ser vazio
    if tabela.empty:
        raise DadosInvalidosException("DataFrame fornecido está vazio")
    
    # VALIDAÇÃO 2: Deve haver pelo menos uma coluna
    if len(tabela.columns) == 0:
        raise DadosInvalidosException("DataFrame não possui colunas")
    
    # Remover linhas e colunas vazias
    tabela = tabela.dropna(how='all', axis=0)
    tabela = tabela.dropna(how='all', axis=1)
    
    # VALIDAÇÃO 3: Após limpeza, ainda deve haver dados
    if tabela.empty:
        raise DadosInvalidosException("DataFrame contém apenas valores vazios")
    
    # Separa os erros dos dados da tabela
    erros_list = []
    dados_brutos_list = []

    for coluna in tabela.columns:
        if eh_erro_instrumental(str(coluna)):
            erros_list.append(coluna)
        else:
            dados_brutos_list.append(coluna)
    
    # VALIDAÇÃO 4: Deve haver ao menos uma coluna de dados
    if not dados_brutos_list:
        raise ColunasInvalidasException("Nenhuma coluna de dados encontrada")
    
    logger.info(f"Particionamento: {len(dados_brutos_list)} colunas de dados, "
                f"{len(erros_list)} colunas de erro")
    

    # Inicializa dicionários de resultados
    erros_instrumentais_list = [float('nan')]
    dados_keys = []
    dados_iteracoes = {}
    dados_brutos = {}
    erros_instrumentais = {}

    for coluna in tabela.columns:
        if eh_erro_instrumental(coluna):
            
            # VALIDAÇÃO 5: Verificar se dados são numéricos
            dados_serie = tabela[coluna].dropna()
            try:
                erros_instrumentais_list = pd.to_numeric(dados_serie).tolist()
            except (ValueError, TypeError) as e:
                logger.warning(f"Coluna '{coluna}' contém dados não numéricos, ignorando")
                continue
                
        else:
            if 'dados' in str(coluna).lower():
                dados_keys = tabela[coluna].dropna().tolist()
            else:
                # VALIDAÇÃO 5: Verificar se dados são numéricos
                dados_serie = tabela[coluna].dropna()
                try:
                    dados_iteracoes[coluna] = pd.to_numeric(dados_serie).tolist()
                except (ValueError, TypeError) as e:
                    logger.warning(f"Coluna '{coluna}' contém dados não numéricos, ignorando")
                continue
            

    for key in dados_keys:
        dados_brutos[key] = []
        erros_instrumentais[key] = []
        for coluna in dados_iteracoes:
            dados_brutos[key].append(dados_iteracoes[coluna][dados_keys.index(key)])
        erros_instrumentais[key].append(erros_instrumentais_list[dados_keys.index(key)])

    # VALIDAÇÃO 6: Deve restar ao menos uma coluna após conversão
    if not dados_brutos:
        raise DadosInvalidosException("Nenhuma coluna contém dados numéricos válidos")

    return dados_brutos, erros_instrumentais, dados_keys


def calcular_estatisticas(tabela: pd.DataFrame):
    """
    Calcula a média, erro estatístico e erro total dos dados.
    
    Retorna uma nova tabela, contendo o nome dos dados, a média, o erro estatístico e o erro total.
    
    Args:
        tabela (pd.DataFrame): DataFrame com os dados e erros instrumentais
        
    Returns:
        pd.DataFrame: DataFrame com as colunas ['Dados', 'Média', 'S_err', 'T_err']
    """

    # VALIDAÇÃO PRÉVIA
    if tabela.empty:
        raise DadosInvalidosException("DataFrame vazio fornecido")

    # Particiona os dados brutos e erros instrumentais
    dados_brutos, erros_instr, dados_keys = particionar(tabela)

    # VALIDAÇÃO: Verificar se há dados suficientes
    total_medicoes = sum(len(valores) for valores in dados_brutos.values())
    if total_medicoes == 0:
        raise DadosInsuficientesException("Nenhuma medição encontrada nos dados")
    
    logger.info(f"Calculando estatísticas para {len(dados_brutos)} variáveis")

    # Inicializa dicionários de resultados
    medias = {}
    erros_est = {}
    erros_totais = {}

    # Calcula a média dos elementos
    for key in dados_brutos:
        medias[key] = float(sum(dados_brutos[key])) / float(len(dados_brutos[key]))

    # Calcula o erro estatístico e erro total para cada chave
    for key, valores in dados_brutos.items():
        desvio_padrao = {}
        desvio_padrao[key] = (sum([(x - medias[key]) ** 2 for x in valores]) / (len(valores)-1)) ** 0.5

        erros_est[key] = desvio_padrao[key] / (len(valores) ** 0.5)
        erros_totais[key] = (erros_est[key] ** 2 + erros_instr[key] ** 2) ** 0.5
    
    # Monta o DataFrame de resultados
    resultado = pd.DataFrame({
        'Dados': list(dados_keys),
        'Média': [medias[key] for key in dados_keys],
        'S_err': [erros_est[key] for key in dados_keys],
        'T_err': [erros_totais[key] for key in dados_keys]
    })

    return resultado
