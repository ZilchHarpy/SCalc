"""
Modulo de parsing e extracao de informacoes de nomes de colunas em DataFrames.
"""

import re
from typing import Optional

# Indicadores de erro e instrumental usados em eh_erro_instrumental().
# Checagem de erro e feita por substring (para capturar 'xerr', 'ierr', etc.).
# Checagem de instrumental e feita por token exato apos split por separadores
# (_-\s), o que evita falsos positivos pela letra 'i' embutida em palavras
# como 'distancia' ou 'medicao'.
_INDICADORES_ERRO  = {'err', 'error', 'erro'}
_INDICADORES_INSTR = {'i', 'instr', 'ins', 'instrumental', 'instrument'}


def contar(prefixo: str, lista: list) -> int:
    """
    Conta quantos itens em uma lista comecam com um prefixo especifico
    seguido de um separador reconhecido (_  -  espaco  newline).

    O separador e obrigatorio para evitar que prefixos sejam encontrados
    como substrings de nomes mais longos. Por exemplo, contar('temp', ...)
    nao conta 'temperatura_1'.

    Args:
        prefixo (str): Prefixo a procurar
        lista (list[str]): Lista de strings a analisar

    Returns:
        int: Quantidade de itens que comecam com o prefixo seguido de separador

    Examples:
        >>> contar('a', ['a_1', 'a_2', 'b_1'])
        2
        >>> contar('temp', ['temperatura_1', 'temp_1'])
        1
    """
    separadores = ('_', ' ', '-', '\n')
    return sum(
        1 for item in lista
        if any(item.startswith(prefixo + sep) for sep in separadores)
    )


def extrair_prefixo(nome) -> Optional[str]:
    """
    Extrai o prefixo alfabetico inicial de uma string.

    Args:
        nome: Valor a analisar (qualquer tipo; retorna None se nao for str)

    Returns:
        str: Sequencia alfabetica inicial, ou None se nao encontrada

    Examples:
        >>> extrair_prefixo('a_1')
        'a'
        >>> extrair_prefixo('temperatura2')
        'temperatura'
        >>> extrair_prefixo('123')
        None
        >>> extrair_prefixo(None)
        None
    """
    if not isinstance(nome, str):
        return None

    match = re.match(r'^([a-zA-Z]+)', nome.strip())
    return match.group(1) if match else None


def eh_erro_instrumental(nome_coluna) -> bool:
    """
    Verifica se um nome de coluna representa um erro instrumental.

    A deteccao exige duas condicoes simultaneas:
    - Indicador de ERRO: a string contem como substring algum de
      {'err', 'error', 'erro'} (case-insensitive). Substring e usada
      para capturar padroes como 'xerr' ou 'ierr'.
    - Indicador de INSTRUMENTAL: algum token gerado pelo split por
      separadores (_-\s) e exatamente um de {'i', 'instr', 'ins',
      'instrumental', 'instrument'} (case-insensitive). Token exato
      e usado para evitar falso positivo pela letra 'i' embutida em
      palavras como 'distancia' ou 'medicao'.

    Args:
        nome_coluna: Valor a analisar (qualquer tipo)

    Returns:
        bool: True se for coluna de erro instrumental

    Examples:
        >>> eh_erro_instrumental('I_err')
        True
        >>> eh_erro_instrumental('xerr_instr')
        True
        >>> eh_erro_instrumental('distancia_err')   # i dentro de palavra -> False
        False
        >>> eh_erro_instrumental('y1')
        False
    """
    if not isinstance(nome_coluna, str):
        return False

    lower = nome_coluna.lower()
    tokens = set(re.split(r'[_\-\s]+', lower))

    tem_erro  = any(ind in lower   for ind in _INDICADORES_ERRO)
    tem_instr = bool(tokens & _INDICADORES_INSTR)

    return tem_erro and tem_instr
