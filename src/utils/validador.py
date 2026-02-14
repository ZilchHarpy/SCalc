"""
Modulo de Validacao de Dados

Contem a classe ValidadorDados para centralizar todas as validacoes
de entrada e processamento de dados do SCalc.
"""

import pandas as pd
import logging
from typing import Tuple, Dict, List, Any, Optional

from src.core.exceptions import (
    DadosInvalidosException,
    DadosInsuficientesException,
    DadosNaoNumericosException,
    ArquivoInvalidoException
)
from src.data.config import Config

logger = logging.getLogger(__name__)


class ValidadorDados:
    """Validador centralizado para dados do SCalc"""
    
    @staticmethod
    def validar_dataframe(df: pd.DataFrame, nome: str = "DataFrame") -> bool:
        """
        Valida um DataFrame basico
        
        Args:
            df: DataFrame a validar
            nome: Nome do DataFrame para mensagens de erro
            
        Returns:
            bool: True se valido
            
        Raises:
            DadosInvalidosException: Se o DataFrame for invalido
        """
        if not isinstance(df, pd.DataFrame):
            raise DadosInvalidosException(f"{nome} deve ser um pd.DataFrame")
        
        if df.empty:
            raise DadosInvalidosException(f"{nome} esta vazio")
        
        if len(df.columns) == 0:
            raise DadosInvalidosException(f"{nome} nao possui colunas")
        
        logger.info(f"DataFrame '{nome}' validado: {len(df)} linhas, {len(df.columns)} colunas")
        return True
    
    @staticmethod
    def validar_arquivo_excel(caminho: str) -> bool:
        """
        Valida se arquivo Excel existe e e acessivel
        
        Args:
            caminho: Caminho do arquivo
            
        Returns:
            bool: True se valido
            
        Raises:
            ArquivoInvalidoException: Se arquivo for invalido
        """
        import os
        
        if not os.path.exists(caminho):
            raise ArquivoInvalidoException(f"Arquivo nao encontrado: {caminho}")
        
        if not caminho.lower().endswith(('.xlsx', '.xls')):
            raise ArquivoInvalidoException(f"Arquivo deve ser Excel (.xlsx ou .xls): {caminho}")
        
        tamanho_mb = os.path.getsize(caminho) / (1024 * 1024)
        if tamanho_mb > Config.Validacao.MAX_TAMANHO_ARQUIVO_MB:
            raise ArquivoInvalidoException(
                f"Arquivo excede tamanho maximo de {Config.Validacao.MAX_TAMANHO_ARQUIVO_MB}MB"
            )
        
        logger.info(f"Arquivo '{caminho}' validado ({tamanho_mb:.2f}MB)")
        return True
    
    @staticmethod
    def validar_dados_numericos(
        serie: pd.Series,
        nome_coluna: str = "coluna"
    ) -> pd.Series:
        """
        Valida se serie contem dados numericos
        
        Args:
            serie: Serie a validar
            nome_coluna: Nome da coluna para mensagens
            
        Returns:
            pd.Series: Serie convertida para numerico
            
        Raises:
            DadosNaoNumericosException: Se contiver dados nao numericos
        """
        try:
            dados_numericos = pd.to_numeric(serie, errors='coerce')
            
            if dados_numericos.isna().all():
                raise DadosNaoNumericosException(
                    f"Coluna '{nome_coluna}' contem apenas valores nao numericos"
                )
            
            nans_removidos = serie.isna().sum() - dados_numericos.isna().sum()
            if nans_removidos > 0:
                logger.warning(
                    f"Coluna '{nome_coluna}': {nans_removidos} valores nao numericos ignorados"
                )
            
            return dados_numericos
            
        except Exception as e:
            raise DadosNaoNumericosException(
                f"Erro ao processar coluna '{nome_coluna}': {str(e)}"
            )
    
    @staticmethod
    def validar_medicoes_minimas(
        dados: Dict[str, List[float]],
        minimo: int | None = None
    ) -> bool:
        """
        Valida se ha minimo de medicoes recomendado
        
        Args:
            dados: Dicionario de dados
            minimo: Minimo de medicoes (padrao: Config.Estatistica.MIN_MEDICOES_RECOMENDADO)
            
        Returns:
            bool: True se ha medicoes suficientes
            
        Raises:
            DadosInsuficientesException: Se insuficiente
        """
        if minimo is None:
            minimo = Config.Estatistica.MIN_MEDICOES_RECOMENDADO
        
        total_medicoes = sum(len(valores) for valores in dados.values())
        
        if total_medicoes == 0:
            raise DadosInsuficientesException("Nenhuma medicao encontrada nos dados")
        
        if total_medicoes < minimo:
            raise DadosInsuficientesException(
                f"Minimo de {minimo} medicoes recomendado, encontrado: {total_medicoes}"
            )
        
        logger.info(f"Validacao de medicoes: {total_medicoes} encontradas (minimo: {minimo})")
        return True
    
    @staticmethod
    def validar_tamanho_arquivo(
        df: pd.DataFrame,
        max_linhas: int | None = None,
        max_colunas: int | None = None
    ) -> bool:
        """
        Valida se arquivo esta dentro dos limites de tamanho
        
        Args:
            df: DataFrame
            max_linhas: Maximo de linhas (padrao: Config)
            max_colunas: Maximo de colunas (padrao: Config)
            
        Returns:
            bool: True se dentro dos limites
            
        Raises:
            DadosInvalidosException: Se exceder limites
        """
        if max_linhas is None:
            max_linhas = Config.Validacao.MAX_LINHAS
        if max_colunas is None:
            max_colunas = Config.Validacao.MAX_COLUNAS
        
        if len(df) > max_linhas:
            raise DadosInvalidosException(
                f"Arquivo excede limite de {max_linhas} linhas ({len(df)} encontradas)"
            )
        
        if len(df.columns) > max_colunas:
            raise DadosInvalidosException(
                f"Arquivo excede limite de {max_colunas} colunas ({len(df.columns)} encontradas)"
            )
        
        return True
