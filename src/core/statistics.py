"""
Modulo de Estatistica

Contem funcoes para calculo de media, erro estatistico, erro instrumental
e erro total a partir de dados em DataFrame.
"""

import logging
import pandas as pd
import numpy as np
from collections import defaultdict
import re
import math

from src.utils.parsers import eh_erro_instrumental, extrair_prefixo
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
    Particiona a tabela em dicionarios especificos para auxilio nas operacoes de estatistica.
    
    Args:
        tabela (pd.DataFrame): DataFrame com os dados completos
        
    Returns:
        tuple: (dados_brutos, erros_instrumentais, dados_keys) - dicionarios de retorno contendo:
            dados_brutos (dict): Dicionario geral dos dados, organizado por chave e coluna
            erros_instrumentais (dict): Dicionario dos erros instrumentais, organizado por chave
            dados_keys (dict): Dicionario das chaves iteradas, mapeando chave com quantidade de iteracoes
    
    Raises:
        DadosInvalidosException: Se DataFrame for invalido
        ColunasInvalidasException: Se nao houver colunas de dados validas
    
    Examples:
        >>> tabela = pd.DataFrame({
        ...     'Dados': ['a_1', 'a_2', 'a_3', 'b_1', 'b_2', 'b_3', 'c_1', 'c_2', 'c_3'],
        ...     'I_err': [0.01, 0.02, 0.03, 0.01, 0.02, 0.03, 0.5, 0.6, 0.7],
        ...     '1': [1, 4, 8, 1, 4, 8, 100, 200, 300],
        ...     '2': [2, 5, 9, 2, 5, 9, None, None, None],
        ...     '3': [3, 6, 10, 3, 6, 10, None, None, None]
        ... })
        >>> dados_brutos, erros_instrumentais, chaves_iteradas = particionar(tabela)
        >>> dados_brutos
        ... {'a': {'a_1': [1, 2, 3], 'a_2': [4, 5, 6], 'a_3': [8, 9, 10]},
        ... 'b': {'b_1': [1, 2, 3], 'b_2': [4, 5, 6], 'b_3': [8, 9, 10]},
        ... 'c': {'c_1': [100], 'c_2': [200], 'c_3': [300]}
        ... }
        >>> erros_instrumentais
        ... {'a': {'a_1': 0.01, 'a_2': 0.02, 'a_3': 0.03},
        ... 'b': {'b_1': 0.01, 'b_2': 0.02, 'b_3': 0.03},
        ... 'c': {'c_1': 0.5, 'c_2': 0.6, 'c_3': 0.7}
        ... }
        >>> chaves_iteradas
        {'a': 3, 'b': 3, 'c': 3}
    """
    # Validacoes iniciais
    ValidadorDados.validar_dataframe(tabela, "Tabela de entrada")
    
    # Remover linhas e colunas vazias
    tabela = tabela.dropna(how='all', axis=0)
    tabela = tabela.dropna(how='all', axis=1)
    
    if tabela.empty:
        raise DadosInvalidosException("DataFrame contem apenas valores vazios apos limpeza")
    
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
    
    # Inicializa dicionarios de resultados
    erros_instrumentais_list = [float('nan')]
    erros_instrumentais_iteracoes = defaultdict(list)
    lista_dados = defaultdict(list)
    dados_keys = {}
    dados_iteracoes = defaultdict(list)
    dados_brutos = {}
    erros_instrumentais = {}

    for coluna in tabela.columns:
        if eh_erro_instrumental(coluna):
            # Validar dados numericos
            try:
                dados_serie = ValidadorDados.validar_dados_numericos(
                    tabela[coluna], 
                    str(coluna)
                )
                erros_instrumentais_list = dados_serie.dropna().tolist()
                for i, k in enumerate(erros_instrumentais_list):
                    erros_instrumentais_iteracoes[lista_dados[i]].append(k)
            except DadosNaoNumericosException as e:
                logger.warning(f"Ignorando coluna de erro: {str(e)}")
                continue
                
        else:
            if 'dados' in str(coluna).lower():
                lista_dados = tabela[coluna].dropna().tolist()
                for i, valor in enumerate(lista_dados):
                    chave = extrair_prefixo(valor)
                    if chave:
                        if chave not in dados_keys:
                            dados_keys[chave] = 0
                        dados_keys[chave] += 1
                    else:
                        logger.warning(f"Valor '{valor}' na coluna '{coluna}' nao possui prefixo valido, ignorando")
                    
            else:
                for i, k in enumerate(tabela[coluna].dropna().tolist()):
                    # Validar dados numericos
                    try:
                        dados_serie = ValidadorDados.validar_dados_numericos(
                            tabela[coluna],
                            str(coluna)
                        )
                        dados_iteracoes[lista_dados[i]].append(k)
                    except DadosNaoNumericosException as e:
                        logger.warning(f"Ignorando coluna de dados: {str(e)}")
                        continue

    for key, valor in dados_iteracoes.items():
        if extrair_prefixo(key) in dados_keys:
            prefixo = extrair_prefixo(key)
            if prefixo not in dados_brutos:
                dados_brutos[prefixo] = {}
            dados_brutos[prefixo][key] = valor

            if prefixo not in erros_instrumentais:
                erros_instrumentais[prefixo] = {}
            erro_list = erros_instrumentais_iteracoes[key]
            erros_instrumentais[prefixo][key] = erro_list[0] if erro_list else float('nan')

    if not dados_brutos:
        raise DadosInvalidosException("Nenhuma coluna contem dados numericos validos")

    logger.info(f"Particionamento concluido: {len(dados_brutos)} variaveis extraidas")
    return dados_brutos, erros_instrumentais, dados_keys


def calcular_estatisticas(tabela: pd.DataFrame):
    """
    Calcula a media, erro estatistico e erro total dos dados.
    
    Retorna uma nova tabela, contendo o nome dos dados, a media, o erro estatistico e o erro total.
    
    Args:
        tabela (pd.DataFrame): DataFrame com os dados e erros instrumentais
        
    Returns:
        pd.DataFrame: DataFrame com as colunas ['Dados', 'Media', 'S_err', 'T_err']
        
    Raises:
        DadosInvalidosException: Se DataFrame for invalido
        DadosInsuficientesException: Se nao houver medicoes suficientes
    """
    # Validacao previa
    ValidadorDados.validar_dataframe(tabela, "Tabela de estatisticas")

    # Particiona os dados brutos e erros instrumentais
    dados_brutos, erros_instr, dados_keys = particionar(tabela)

    # Validar dados suficientes
    # Verifica se ha dados em algum prefixo
    if not dados_brutos or all(not v for v in dados_brutos.values()):
        raise DadosInvalidosException("Nenhuma coluna contem dados numericos validos")
    
    total_medicoes = sum(
        sum(len(valores) for valores in prefixo_dados.values())
        for prefixo_dados in dados_brutos.values()
    )
    
    if total_medicoes == 0:
        raise DadosInsuficientesException("Nenhuma medicao disponivel")
    
    logger.info(f"Calculando estatisticas para {len(dados_keys)} grupos ({total_medicoes} medicoes)")

    # Inicializa listas de resultados
    dados_nomes = []
    medias = []
    erros_est = []
    erros_totais = []

    # Calcula estatisticas para cada chave de dado (a_1, a_2, etc)
    for prefixo, prefixo_dados in dados_brutos.items():
        for chave, valores in sorted(prefixo_dados.items()):
            if not valores:
                continue
                
            # Calcula media
            media = float(sum(valores)) / float(len(valores))
            
            # Calcula desvio padrao
            if len(valores) > 1:
                desvio_padrao = (sum([(x - media) ** 2 for x in valores]) / (len(valores) - 1)) ** 0.5
                erro_estatistico = desvio_padrao / (len(valores) ** 0.5)
            else:
                erro_estatistico = 0.0
            
            # Obtem erro instrumental (agora eh um float direto)
            erro_instrumental = erros_instr[prefixo][chave]
            
            # Calcula erro total
            erro_total = (erro_estatistico ** 2 + erro_instrumental ** 2) ** 0.5
            
            # Armazena resultados
            dados_nomes.append(chave)
            medias.append(media)
            erros_est.append(erro_estatistico)
            erros_totais.append(erro_total)
    
    logger.debug(f"Medias calculadas: {list(zip(dados_nomes, medias))}")
    logger.debug(f"Erros estatisticos: {list(zip(dados_nomes, erros_est))}")
    logger.debug(f"Erros totais: {list(zip(dados_nomes, erros_totais))}")
    
    # Monta o DataFrame de resultados
    resultado = pd.DataFrame({
        'Dados': dados_nomes,
        'Media': medias,
        'S_err': erros_est,
        'T_err': erros_totais
    })

    logger.info(f"Estatisticas calculadas com sucesso para {len(resultado)} variaveis")
    return resultado
