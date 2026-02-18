"""
Modulo de parsing e extracao de informacoes de nomes de colunas em DataFrames.
"""

import re
from typing import Optional

def contar(prefixo, lista):
    """
    Conta quantos itens em uma lista comecam com um prefixo especifico

    Args:
        prefixo (str): Prefixo a procurar
        lista (list[str]): Lista de string a analisar
    """
    return sum(1 for item in lista if (
                                        item.startswith(prefixo + "_") or
                                        item.startswith(prefixo + " ") or
                                        item.startswith(prefixo + "-") or
                                        item.startswith(prefixo + "\n") or
                                        item.startswith(prefixo + "")))

def extrair_prefixo(nome) -> Optional[str]:
    """
    Extrai o prefixo alfabetico de uma coluna (ex: 'x1' -> 'x'; 'temp2' -> 'temp)

    Args:
        nome_coluna (str): Nome da coluna a analisar
    
    Returns:
        str: Prefixo da variavel, ou None se nao encontrado
    
    Examples:
        >>> extrair_prefixo('x1')
        'x'
        >>> extrair_prefixo('i_err')
        'i'
        >>> extrair_prefixo('temperatura2')
        'temperatura'
        >>> extrair_prefixo('123')
        None
    """
    if not isinstance(nome, str):
        return None
    
    match = re.match(r'^([a-zA-Z]+)', nome.strip())
    return match.group(1) if match else None

def eh_erro_instrumental(nome_coluna) -> bool:
    """
    verifica se uma coluna representa um erro instrumental

    Args:
        nome_coluna (str): Nome da coluna a analisar

    Returns:
        bool: True se for coluna de erro instrumental, False caso contrario

    Examples:
        >>> eh_erro_instrumental('i_err')
        True
        >>> eh_erro_instrumental('I_Err')
        True
        >>> eh_erro_instrumental('y1')
        False
    """
    if not isinstance(nome_coluna, str):
        return False
    
    return ('err' in nome_coluna.lower() or 'error' in nome_coluna.lower() or 'erro' in nome_coluna.lower()) and ('i' in nome_coluna.lower() or 'instr' in nome_coluna.lower()  or 'ins' in nome_coluna.lower() or 'instrumental' in nome_coluna.lower() or 'instrument' in nome_coluna.lower())
