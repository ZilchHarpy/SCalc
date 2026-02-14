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

from src.utils.parsers import eh_erro_instrumental
from src.utils.validador import ValidadorDados
from src.core.exceptions import (
    DadosInvalidosException,
    DadosInsuficientesException,
    ColunasInvalidasException,
    DadosNaoNumericosException
)

# Configura o logger
logger = logging.getLogger(__name__)

def particionar(tabela: pd.DataFrame):
    """
    Particiona a tabela em dicionários de dados brutos e erros instrumentais.
    
    Args:
        tabela (pd.DataFrame): DataFrame com os dados completos
        
    Returns:
        tuple: (dados_brutos, erros_instrumentais, dados_keys) - dicionários com dados, 
               erros instrumentais e lista de chaves
    
    Raises:
        DadosInvalidosException: Se DataFrame for inválido
        ColunasInvalidasException: Se não houver colunas de dados válidas
    
    Examples:
        >>> tabela = pd.DataFrame({
        ...     'Dados': ['a', 'b', 'c', 'd'],
        ...     'I_err': [0.01, 0.02, 0.015, 0.01],
        ...     '1': [1, 2, 3],
        ...     '2': [4, 5, 6],
        ...     '3': [7, 8, 9]
        ... })
        >>> dados, erros_instrumentais, chaves = particionar(tabela)
        >>> dados
        {'a': [1, 4, 7], 'b': [2, 5, 8], 'c': [3, 6, 9]}
    """
    # Validações iniciais
    ValidadorDados.validar_dataframe(tabela, "Tabela de entrada")
    
    # Remover linhas e colunas vazias
    tabela = tabela.dropna(how='all', axis=0)
    tabela = tabela.dropna(how='all', axis=1)
    
    if tabela.empty:
        raise DadosInvalidosException("DataFrame contém apenas valores vazios após limpeza")
    
    # Separar erros dos dados
    erros_list = []
    dados_brutos_list = []

    for coluna in tabela.columns:
        if eh_erro_instrumental(str(coluna)):
            erros_list.append(coluna)
        else:
            dados_brutos_list.append(coluna)
    
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
            # Validar dados numéricos
            try:
                dados_serie = ValidadorDados.validar_dados_numericos(
                    tabela[coluna], 
                    str(coluna)
                )
                erros_instrumentais_list = dados_serie.dropna().tolist()
            except DadosNaoNumericosException as e:
                logger.warning(f"Ignorando coluna de erro: {str(e)}")
                continue
                
        else:
            if 'dados' in str(coluna).lower():
                dados_keys = tabela[coluna].dropna().tolist()
            else:
                # Validar dados numéricos
                try:
                    dados_serie = ValidadorDados.validar_dados_numericos(
                        tabela[coluna],
                        str(coluna)
                    )
                    dados_iteracoes[coluna] = dados_serie.dropna().tolist()
                except DadosNaoNumericosException as e:
                    logger.warning(f"Ignorando coluna de dados: {str(e)}")
                    continue
            

    for key in dados_keys:
        dados_brutos[key] = []
        erros_instrumentais[key] = []
        for coluna in dados_iteracoes:
            dados_brutos[key].append(dados_iteracoes[coluna][dados_keys.index(key)])
        erros_instrumentais[key].append(erros_instrumentais_list[dados_keys.index(key)])

    if not dados_brutos:
        raise DadosInvalidosException("Nenhuma coluna contém dados numéricos válidos")

    logger.info(f"Particionamento concluído: {len(dados_brutos)} variáveis extraídas")
    return dados_brutos, erros_instrumentais, dados_keys


def calcular_estatisticas(tabela: pd.DataFrame):
    """
    Calcula a média, erro estatístico e erro total dos dados.
    
    Retorna uma nova tabela, contendo o nome dos dados, a média, o erro estatístico e o erro total.
    
    Args:
        tabela (pd.DataFrame): DataFrame com os dados e erros instrumentais
        
    Returns:
        pd.DataFrame: DataFrame com as colunas ['Dados', 'Média', 'S_err', 'T_err']
        
    Raises:
        DadosInvalidosException: Se DataFrame for inválido
        DadosInsuficientesException: Se não houver medições suficientes
    """
    # Validação prévia
    ValidadorDados.validar_dataframe(tabela, "Tabela de estatísticas")

    # Particiona os dados brutos e erros instrumentais
    dados_brutos, erros_instr, dados_keys = particionar(tabela)

    # Validar dados suficientes
    ValidadorDados.validar_medicoes_minimas(dados_brutos)
    
    total_medicoes = sum(len(valores) for valores in dados_brutos.values())
    logger.info(f"Calculando estatísticas para {len(dados_brutos)} variáveis ({total_medicoes} medições)")

    # Inicializa dicionários de resultados
    medias = {}
    erros_est = {}
    erros_totais = {}

    # Calcula a média dos elementos
    for key in dados_brutos:
        medias[key] = float(sum(dados_brutos[key])) / float(len(dados_brutos[key]))

    logger.debug(f"Médias calculadas: {medias}")

    # Calcula o erro estatístico e erro total para cada chave
    for key, valores in dados_brutos.items():
        desvio_padrao = {}
        desvio_padrao[key] = (sum([(x - medias[key]) ** 2 for x in valores]) / (len(valores)-1)) ** 0.5

        erros_est[key] = desvio_padrao[key] / (len(valores) ** 0.5)
        erros_totais[key] = (erros_est[key] ** 2 + erros_instr[key][0] ** 2) ** 0.5
    
    logger.debug(f"Erros estatísticos: {erros_est}")
    logger.debug(f"Erros totais: {erros_totais}")
    
    # Monta o DataFrame de resultados
    resultado = pd.DataFrame({
        'Dados': list(dados_keys),
        'Média': [medias[key] for key in dados_keys],
        'S_err': [erros_est[key] for key in dados_keys],
        'T_err': [erros_totais[key] for key in dados_keys]
    })

    logger.info(f"Estatísticas calculadas com sucesso para {len(resultado)} variáveis")
    return resultado
