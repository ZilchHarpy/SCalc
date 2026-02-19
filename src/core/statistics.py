"""
Modulo de Estatistica

Contem funcoes para calculo de media, erro estatistico, erro instrumental
e erro total a partir de dados em DataFrame.
"""

import logging
import math
import pandas as pd
from collections import defaultdict

from src.utils.parsers import eh_erro_instrumental, extrair_prefixo
from src.utils.validador import ValidadorDados
from src.core.exceptions import (
    DadosInvalidosException,
    DadosInsuficientesException,
    ColunasInvalidasException,
    DadosNaoNumericosException,
)

logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------- #
#  Helper interno (exportado para evitar duplicacao em scalc.py)              #
# --------------------------------------------------------------------------- #

def calcular_stats_prefixo(
    dados_por_chave: dict,
    erros_por_chave: dict,
) -> tuple:
    """
    Calcula medias e erros totais para um unico grupo (prefixo).

    Centraliza a logica de calculo usada por calcular_estatisticas() e pelo
    modo CLI em scalc.py, evitando duplicacao de codigo.

    Args:
        dados_por_chave (dict[str, list[float]]): mapeamento chave -> repeticoes.
            Ex: {'a_1': [1.0, 1.1, 0.9], 'a_2': [2.0, 2.1, 1.9]}
        erros_por_chave (dict[str, float]): mapeamento chave -> erro instrumental.
            Ex: {'a_1': 0.10, 'a_2': 0.10}

    Returns:
        tuple[list[float], list[float]]: (medias, erros_totais) em ordem
            alfabetica de chaves. Chaves sem valores sao ignoradas.

    Notes:
        Erro estatistico  = desvio_padrao_amostral / sqrt(n)  (n > 1)
                          = 0.0                               (n == 1)
        Erro total        = sqrt(erro_estatistico^2 + erro_instrumental^2)
    """
    medias: list = []
    erros_totais: list = []

    for chave in sorted(dados_por_chave.keys()):
        valores = dados_por_chave[chave]
        if not valores:
            continue

        n = len(valores)
        media = sum(valores) / n

        if n > 1:
            variancia = sum((v - media) ** 2 for v in valores) / (n - 1)
            erro_est = math.sqrt(variancia) / math.sqrt(n)
        else:
            erro_est = 0.0

        i_err = erros_por_chave.get(chave, 0.0)
        if isinstance(i_err, float) and math.isnan(i_err):
            i_err = 0.0

        t_err = math.sqrt(erro_est ** 2 + i_err ** 2)

        medias.append(media)
        erros_totais.append(t_err)

    return medias, erros_totais


# --------------------------------------------------------------------------- #
#  particionar                                                                 #
# --------------------------------------------------------------------------- #

def particionar(tabela: pd.DataFrame):
    """
    Particiona a tabela em dicionarios especificos para auxilio nas operacoes
    de estatistica.

    A funcao realiza duas passagens sobre as colunas:
    - Passagem 1: localiza a coluna de identificadores (nome contem 'dados')
      e popula lista_dados e dados_keys.
    - Passagem 2: processa colunas de erro instrumental e colunas numericas,
      usando lista_dados ja preenchida.

    Isso garante que a ordem das colunas no arquivo Excel nao afete o
    resultado (I_err pode vir antes ou depois de Dados).

    Args:
        tabela (pd.DataFrame): DataFrame com os dados completos.

    Returns:
        tuple: (dados_brutos, erros_instrumentais, dados_keys)

            dados_brutos (dict[str, dict[str, list[float]]]):
                Agrupado por prefixo, depois por chave.
                Ex: {'a': {'a_1': [1.0, 1.1], 'a_2': [2.0, 2.1]}, ...}

            erros_instrumentais (dict[str, dict[str, float]]):
                Agrupado por prefixo, depois por chave.
                Ex: {'a': {'a_1': 0.10, 'a_2': 0.10}, ...}

            dados_keys (dict[str, int]):
                Contagem de pontos por prefixo.
                Ex: {'a': 2, 'b': 2}

    Raises:
        DadosInvalidosException: DataFrame invalido, so NaN, ou sem dados
            numericos validos apos o particionamento.
        ColunasInvalidasException: Todas as colunas foram classificadas como
            erro instrumental (nenhuma coluna de dados restante).

    Examples:
        >>> tabela = pd.DataFrame({
        ...     'Dados': ['a_1', 'a_2', 'b_1', 'b_2'],
        ...     'I_err': [0.10, 0.10, 0.20, 0.20],
        ...     '1':     [1.0,  2.0,  2.0,  4.0],
        ...     '2':     [1.1,  2.1,  2.1,  4.1],
        ... })
        >>> dados_brutos, erros, keys = particionar(tabela)
        >>> dados_brutos['a']['a_1']
        [1.0, 1.1]
        >>> erros['a']['a_1']
        0.10
        >>> keys
        {'a': 2, 'b': 2}
    """
    # ------------------------------------------------------------------ #
    #  Validacao e limpeza inicial                                         #
    # ------------------------------------------------------------------ #
    ValidadorDados.validar_dataframe(tabela, "Tabela de entrada")

    tabela = tabela.dropna(how='all', axis=0).dropna(how='all', axis=1)

    if tabela.empty:
        raise DadosInvalidosException(
            "DataFrame contem apenas valores vazios apos limpeza"
        )

    colunas_dados = [
        c for c in tabela.columns if not eh_erro_instrumental(str(c))
    ]
    if not colunas_dados:
        raise ColunasInvalidasException("Nenhuma coluna de dados encontrada")

    logger.info(
        f"Particionamento: {len(colunas_dados)} colunas de dados, "
        f"{len(tabela.columns) - len(colunas_dados)} colunas de erro"
    )

    # ------------------------------------------------------------------ #
    #  Passagem 1: popular lista_dados e dados_keys                        #
    # ------------------------------------------------------------------ #
    lista_dados: list = []   # lista posicional dos identificadores (ex: 'a_1')
    dados_keys:  dict = {}   # contagem de pontos por prefixo

    for coluna in tabela.columns:
        if not eh_erro_instrumental(str(coluna)) and 'dados' in str(coluna).lower():
            lista_dados = tabela[coluna].dropna().tolist()
            for valor in lista_dados:
                prefixo = extrair_prefixo(str(valor))
                if prefixo:
                    dados_keys[prefixo] = dados_keys.get(prefixo, 0) + 1
                else:
                    logger.warning(
                        f"Valor '{valor}' na coluna '{coluna}' "
                        f"nao possui prefixo valido, ignorando"
                    )
            break  # apenas uma coluna de identificadores e esperada

    # ------------------------------------------------------------------ #
    #  Passagem 2: processar erros e colunas numericas                    #
    # ------------------------------------------------------------------ #
    erros_instrumentais_iteracoes: dict = defaultdict(list)
    dados_iteracoes:               dict = defaultdict(list)

    for coluna in tabela.columns:
        coluna_str = str(coluna)

        if eh_erro_instrumental(coluna_str):
            try:
                serie = ValidadorDados.validar_dados_numericos(
                    tabela[coluna], coluna_str
                )
                valores_erro = serie.dropna().tolist()
                for i, v in enumerate(valores_erro):
                    if i < len(lista_dados):
                        erros_instrumentais_iteracoes[lista_dados[i]].append(v)
            except DadosNaoNumericosException as e:
                logger.warning(f"Ignorando coluna de erro: {e}")

        elif 'dados' not in coluna_str.lower():
            # Coluna numerica de repeticoes
            try:
                serie = ValidadorDados.validar_dados_numericos(
                    tabela[coluna], coluna_str
                )
                valores_col = tabela[coluna].dropna()
                # Itera pelos indices originais para manter o mapeamento
                # com lista_dados mesmo quando ha NaN intercalados
                idx_limpo = 0
                for idx in tabela.index:
                    val = tabela.at[idx, coluna]
                    if idx_limpo >= len(lista_dados):
                        break
                    import pandas as _pd
                    if not _pd.isna(val):
                        dados_iteracoes[lista_dados[idx_limpo]].append(float(val))
                    idx_limpo += 1
            except DadosNaoNumericosException as e:
                logger.warning(f"Ignorando coluna de dados: {e}")

    # ------------------------------------------------------------------ #
    #  Montar estruturas de saida                                          #
    # ------------------------------------------------------------------ #
    dados_brutos:      dict = {}
    erros_instrumentais: dict = {}

    for chave, valores in dados_iteracoes.items():
        prefixo = extrair_prefixo(str(chave))
        if prefixo not in dados_keys:
            continue

        dados_brutos.setdefault(prefixo, {})[chave] = valores
        erros_instrumentais.setdefault(prefixo, {})

        lista_err = erros_instrumentais_iteracoes.get(chave, [])
        erros_instrumentais[prefixo][chave] = (
            lista_err[0] if lista_err else float('nan')
        )

    if not dados_brutos:
        raise DadosInvalidosException(
            "Nenhuma coluna contem dados numericos validos"
        )

    logger.info(
        f"Particionamento concluido: {len(dados_brutos)} variaveis extraidas"
    )
    return dados_brutos, erros_instrumentais, dados_keys


# --------------------------------------------------------------------------- #
#  calcular_estatisticas                                                       #
# --------------------------------------------------------------------------- #

def calcular_estatisticas(tabela: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula media, erro estatistico e erro total para cada ponto da tabela.

    Internamente chama particionar() e depois calcular_stats_prefixo() para
    cada grupo encontrado.

    Args:
        tabela (pd.DataFrame): DataFrame no formato esperado pelo SCalc.

    Returns:
        pd.DataFrame: Tabela de resultados com as colunas:
            - 'Dados' (str):  identificador do ponto (ex: 'a_1')
            - 'Media' (float): media aritmetica das repeticoes
            - 'S_err' (float): erro estatistico (erro padrao da media)
            - 'T_err' (float): erro total (propagacao quadratica)

    Raises:
        DadosInvalidosException: DataFrame invalido ou sem dados numericos.
        DadosInsuficientesException: Nenhuma medicao disponivel apos o
            particionamento.
    """
    ValidadorDados.validar_dataframe(tabela, "Tabela de estatisticas")

    dados_brutos, erros_instr, dados_keys = particionar(tabela)

    if not dados_brutos or all(not v for v in dados_brutos.values()):
        raise DadosInvalidosException(
            "Nenhuma coluna contem dados numericos validos"
        )

    total_medicoes = sum(
        sum(len(vals) for vals in grupo.values())
        for grupo in dados_brutos.values()
    )
    if total_medicoes == 0:
        raise DadosInsuficientesException("Nenhuma medicao disponivel")

    logger.info(
        f"Calculando estatisticas para {len(dados_keys)} grupos "
        f"({total_medicoes} medicoes)"
    )

    nomes:      list = []
    medias:     list = []
    erros_est:  list = []
    erros_tot:  list = []

    for prefixo, prefixo_dados in dados_brutos.items():
        # calcular_stats_prefixo retorna apenas (medias, erros_totais).
        # Para o DataFrame precisamos tambem dos S_err individuais;
        # calculamos em loop para preservar cada valor separadamente.
        for chave in sorted(prefixo_dados.keys()):
            valores = prefixo_dados[chave]
            if not valores:
                continue

            n = len(valores)
            media = sum(valores) / n

            if n > 1:
                variancia = sum((v - media) ** 2 for v in valores) / (n - 1)
                s_err = math.sqrt(variancia) / math.sqrt(n)
            else:
                s_err = 0.0

            i_err = erros_instr[prefixo].get(chave, 0.0)
            if isinstance(i_err, float) and math.isnan(i_err):
                i_err = 0.0

            t_err = math.sqrt(s_err ** 2 + i_err ** 2)

            nomes.append(chave)
            medias.append(media)
            erros_est.append(s_err)
            erros_tot.append(t_err)

    resultado = pd.DataFrame({
        'Dados': nomes,
        'Media': medias,
        'S_err': erros_est,
        'T_err': erros_tot,
    })

    logger.info(
        f"Estatisticas calculadas com sucesso para {len(resultado)} variaveis"
    )
    return resultado
