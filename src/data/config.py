"""
Modulo de Configuracao

Contem configuracoes globais e caminhos do projeto.
"""

import os
from pathlib import Path
from typing import Dict, Any

class Config:
    """Configuracoes centralizadas do SCalc"""
    
    # ============ INFORMACOES DO PROJETO ============
    APP_NAME = "SCalc"
    APP_VERSION = "1.0.0"
    APP_AUTHOR = "Caio Aquilino Merino"
    APP_DESCRIPTION = "Sistema de Calculo e Analise de Regressao Linear"
    
    # ============ CAMINHOS ============
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    SRC_DIR = PROJECT_ROOT / "src"
    DATA_DIR = SRC_DIR / "data"
    DOCS_DIR = PROJECT_ROOT / "docs"
    EXAMPLES_DIR = PROJECT_ROOT / "examples"
    
    # ============ CONFIGURACOES DE PLOT ============
    class Plot:
        """Configuracoes de plotagem"""
        # Estilo padrao do matplotlib
        STYLE = '_mpl-gallery'
        
        # Tamanho da figura
        FIGURE_WIDTH = 8
        FIGURE_HEIGHT = 6
        FIGURE_DPI = 100
        
        # Cores
        COLOR_PONTOS = 'blue'
        COLOR_ERRO = 'red'
        COLOR_REGRESSAO = 'green'
        
        # Espessuras
        LINEWIDTH_REGRESSAO = 2.0
        MARKERSIZE_PONTOS = 6
        CAPSIZE_ERRO = 5
        
        # Labels padrao
        DEFAULT_X_LABEL = "x"
        DEFAULT_Y_LABEL = "y"
        DEFAULT_TITULO = "Grafico de Dispersao com Regressao Linear"
        
        # Formatos de exportacao suportados
        FORMATOS_EXPORTACAO = ['png', 'pdf', 'svg', 'jpg', 'eps']
    
    # ============ CONFIGURACOES DE ESTATISTICA ============
    class Estatistica:
        """Configuracoes de analise estatistica"""
        # Criterios de qualidade de R2
        R2_EXCELENTE = 0.95
        R2_BOM = 0.85
        R2_MODERADO = 0.70
        
        # Nivel de confianca para erro estatistico (t-Student)
        NIVEL_CONFIANCA = 0.95
        
        # Numero minimo de medicoes recomendado
        MIN_MEDICOES_RECOMENDADO = 3
        
        # Precisao de arredondamento para resultados
        PRECISAO_DECIMAL = 6
    
    # ============ CONFIGURACOES DE VALIDACAO ============
    class Validacao:
        """Configuracoes de validacao de dados"""
        # Tamanho maximo de arquivo Excel (em MB)
        MAX_TAMANHO_ARQUIVO_MB = 50
        
        # Numero maximo de colunas
        MAX_COLUNAS = 100
        
        # Numero maximo de linhas
        MAX_LINHAS = 10000
        
        # Permitir valores faltantes?
        PERMITIR_VALORES_FALTANTES = True
    
    # ============ CONFIGURACOES DE INTERFACE ============
    class UI:
        """Configuracoes de interface grafica"""
        # Tamanho da janela
        WINDOW_WIDTH = 1400
        WINDOW_HEIGHT = 900
        WINDOW_MIN_WIDTH = 1000
        WINDOW_MIN_HEIGHT = 700
        
        # Fontes
        FONT_TITULO_SIZE = 14
        FONT_LABEL_SIZE = 10
        FONT_TEXTO_SIZE = 9
        
        # Temas disponiveis
        TEMAS_DISPONIVEIS = ['claro', 'escuro', 'sistema']
        TEMA_PADRAO = 'sistema'
    
    # ============ CONFIGURACOES DE LOGGING ============
    class Logging:
        """Configuracoes de logging"""
        # Nivel de log padrao
        NIVEL_PADRAO = 'INFO'  # DEBUG, INFO, WARNING, ERROR, CRITICAL
        
        # Formato de log
        FORMATO = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        # Arquivo de log
        ARQUIVO_LOG = Path(__file__).parent.parent.parent / 'logs' / 'scalc.log'
        
        # Rotacao de logs
        MAX_BYTES = 10 * 1024 * 1024  # 10 MB
        BACKUP_COUNT = 3
    
    # ============ CONFIGURACOES DE INTERNACIONALIZACAO ============
    class I18n:
        """Configuracoes de idioma"""
        IDIOMAS_DISPONIVEIS = ['pt_BR', 'en_US']
        IDIOMA_PADRAO = 'pt_BR'
    
    # ============ METODOS UTILITARIOS ============
    @classmethod
    def get_config_dict(cls) -> Dict[str, Any]:
        """
        Retorna todas as configuracoes como dicionario
        
        Returns:
            dict: Dicionario com todas as configuracoes
        """
        return {
            'app': {
                'name': cls.APP_NAME,
                'version': cls.APP_VERSION,
                'author': cls.APP_AUTHOR,
                'description': cls.APP_DESCRIPTION
            },
            'plot': {
                'style': cls.Plot.STYLE,
                'figure_size': (cls.Plot.FIGURE_WIDTH, cls.Plot.FIGURE_HEIGHT),
                'dpi': cls.Plot.FIGURE_DPI
            },
            'estatistica': {
                'r2_criterios': {
                    'excelente': cls.Estatistica.R2_EXCELENTE,
                    'bom': cls.Estatistica.R2_BOM,
                    'moderado': cls.Estatistica.R2_MODERADO
                }
            }
        }
    
    @classmethod
    def validar_r2(cls, r_squared: float) -> str:
        """
        Classifica a qualidade do ajuste baseado em R2
        
        Args:
            r_squared: Coeficiente de determinacao
            
        Returns:
            str: Classificacao ('excelente', 'bom', 'moderado', 'fraco')
        """
        if r_squared >= cls.Estatistica.R2_EXCELENTE:
            return 'excelente'
        elif r_squared >= cls.Estatistica.R2_BOM:
            return 'bom'
        elif r_squared >= cls.Estatistica.R2_MODERADO:
            return 'moderado'
        else:
            return 'fraco'


# ============ CONFIGURACAO DE LOGGING GLOBAL ============
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(nivel: str | None = None):
    """
    Configura o sistema de logging do SCalc
    
    Args:
        nivel: Nivel de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    if nivel is None:
        nivel = Config.Logging.NIVEL_PADRAO
    
    # Criar diretorio de logs se nao existir
    log_dir = Config.Logging.ARQUIVO_LOG.parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Criar handler para arquivo
    file_handler = RotatingFileHandler(
        Config.Logging.ARQUIVO_LOG,
        maxBytes=Config.Logging.MAX_BYTES,
        backupCount=Config.Logging.BACKUP_COUNT
    )
    file_handler.setFormatter(logging.Formatter(Config.Logging.FORMATO))
    
    # Criar handler para console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(Config.Logging.FORMATO))
    
    # Configurar logger raiz
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, nivel.upper()))
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)


# ============ ALIASES PARA COMPATIBILIDADE ============
# Use a classe Config acima para novas implementacoes
PROJECT_ROOT = Config.PROJECT_ROOT
BASE_DIR = Config.PROJECT_ROOT
SRC_DIR = Config.SRC_DIR
DATA_DIR = Config.DATA_DIR
DOCS_DIR = Config.DOCS_DIR
EXAMPLES_DIR = Config.EXAMPLES_DIR

# Configuracoes da aplicacao (use Config.APP_*)
APP_NAME = Config.APP_NAME
APP_VERSION = Config.APP_VERSION
APP_DESCRIPTION = Config.APP_DESCRIPTION

# Configuracoes de visualizacao (use Config.Plot_*)
PLOT_STYLE = Config.Plot.STYLE
PLOT_DPI = Config.Plot.FIGURE_DPI
PLOT_FIGURE_SIZE = (Config.Plot.FIGURE_WIDTH, Config.Plot.FIGURE_HEIGHT)

# Configuracoes de precisao (use Config.Estatistica.*)
DECIMAL_PLACES = Config.Estatistica.PRECISAO_DECIMAL
R_SQUARED_THRESHOLD_EXCELLENT = Config.Estatistica.R2_EXCELENTE
R_SQUARED_THRESHOLD_GOOD = Config.Estatistica.R2_BOM
R_SQUARED_THRESHOLD_MODERATE = Config.Estatistica.R2_MODERADO
