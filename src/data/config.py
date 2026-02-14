"""
Módulo de Configuração

Contém configurações globais e caminhos do projeto.
"""

import os
from pathlib import Path
from typing import Dict, Any

class Config:
    """Configurações centralizadas do SCalc"""
    
    # ============ INFORMAÇÕES DO PROJETO ============
    APP_NAME = "SCalc"
    APP_VERSION = "1.0.0"
    APP_AUTHOR = "Caio Aquilino Merino"
    APP_DESCRIPTION = "Sistema de Cálculo e Análise de Regressão Linear"
    
    # ============ CAMINHOS ============
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    SRC_DIR = PROJECT_ROOT / "src"
    DATA_DIR = SRC_DIR / "data"
    DOCS_DIR = PROJECT_ROOT / "docs"
    EXAMPLES_DIR = PROJECT_ROOT / "examples"
    
    # ============ CONFIGURAÇÕES DE PLOT ============
    class Plot:
        """Configurações de plotagem"""
        # Estilo padrão do matplotlib
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
        
        # Labels padrão
        DEFAULT_X_LABEL = "log(t) [s]"
        DEFAULT_Y_LABEL = "log(d) [mm]"
        DEFAULT_TITULO = "Gráfico de Dispersão com Regressão Linear"
        
        # Formatos de exportação suportados
        FORMATOS_EXPORTACAO = ['png', 'pdf', 'svg', 'jpg', 'eps']
    
    # ============ CONFIGURAÇÕES DE ESTATÍSTICA ============
    class Estatistica:
        """Configurações de análise estatística"""
        # Critérios de qualidade de R²
        R2_EXCELENTE = 0.95
        R2_BOM = 0.85
        R2_MODERADO = 0.70
        
        # Nível de confiança para erro estatístico (t-Student)
        NIVEL_CONFIANCA = 0.95
        
        # Número mínimo de medições recomendado
        MIN_MEDICOES_RECOMENDADO = 3
        
        # Precisão de arredondamento para resultados
        PRECISAO_DECIMAL = 6
    
    # ============ CONFIGURAÇÕES DE VALIDAÇÃO ============
    class Validacao:
        """Configurações de validação de dados"""
        # Tamanho máximo de arquivo Excel (em MB)
        MAX_TAMANHO_ARQUIVO_MB = 50
        
        # Número máximo de colunas
        MAX_COLUNAS = 100
        
        # Número máximo de linhas
        MAX_LINHAS = 10000
        
        # Permitir valores faltantes?
        PERMITIR_VALORES_FALTANTES = True
    
    # ============ CONFIGURAÇÕES DE INTERFACE ============
    class UI:
        """Configurações de interface gráfica"""
        # Tamanho da janela
        WINDOW_WIDTH = 1400
        WINDOW_HEIGHT = 900
        WINDOW_MIN_WIDTH = 1000
        WINDOW_MIN_HEIGHT = 700
        
        # Fontes
        FONT_TITULO_SIZE = 14
        FONT_LABEL_SIZE = 10
        FONT_TEXTO_SIZE = 9
        
        # Temas disponíveis
        TEMAS_DISPONIVEIS = ['claro', 'escuro', 'sistema']
        TEMA_PADRAO = 'sistema'
    
    # ============ CONFIGURAÇÕES DE LOGGING ============
    class Logging:
        """Configurações de logging"""
        # Nível de log padrão
        NIVEL_PADRAO = 'INFO'  # DEBUG, INFO, WARNING, ERROR, CRITICAL
        
        # Formato de log
        FORMATO = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        # Arquivo de log
        ARQUIVO_LOG = Path(__file__).parent.parent.parent / 'logs' / 'scalc.log'
        
        # Rotação de logs
        MAX_BYTES = 10 * 1024 * 1024  # 10 MB
        BACKUP_COUNT = 3
    
    # ============ CONFIGURAÇÕES DE INTERNACIONALIZAÇÃO ============
    class I18n:
        """Configurações de idioma"""
        IDIOMAS_DISPONIVEIS = ['pt_BR', 'en_US']
        IDIOMA_PADRAO = 'pt_BR'
    
    # ============ MÉTODOS UTILITÁRIOS ============
    @classmethod
    def get_config_dict(cls) -> Dict[str, Any]:
        """
        Retorna todas as configurações como dicionário
        
        Returns:
            dict: Dicionário com todas as configurações
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
        Classifica a qualidade do ajuste baseado em R²
        
        Args:
            r_squared: Coeficiente de determinação
            
        Returns:
            str: Classificação ('excelente', 'bom', 'moderado', 'fraco')
        """
        if r_squared >= cls.Estatistica.R2_EXCELENTE:
            return 'excelente'
        elif r_squared >= cls.Estatistica.R2_BOM:
            return 'bom'
        elif r_squared >= cls.Estatistica.R2_MODERADO:
            return 'moderado'
        else:
            return 'fraco'


# ============ CONFIGURAÇÃO DE LOGGING GLOBAL ============
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(nivel: str | None = None):
    """
    Configura o sistema de logging do SCalc
    
    Args:
        nivel: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    if nivel is None:
        nivel = Config.Logging.NIVEL_PADRAO
    
    # Criar diretório de logs se não existir
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
# Use a classe Config acima para novas implementações
PROJECT_ROOT = Config.PROJECT_ROOT
BASE_DIR = Config.PROJECT_ROOT
SRC_DIR = Config.SRC_DIR
DATA_DIR = Config.DATA_DIR
DOCS_DIR = Config.DOCS_DIR
EXAMPLES_DIR = Config.EXAMPLES_DIR

# Configurações da aplicação (use Config.APP_*)
APP_NAME = Config.APP_NAME
APP_VERSION = Config.APP_VERSION
APP_DESCRIPTION = Config.APP_DESCRIPTION

# Configurações de visualização (use Config.Plot.*)
PLOT_STYLE = Config.Plot.STYLE
PLOT_DPI = Config.Plot.FIGURE_DPI
PLOT_FIGURE_SIZE = (Config.Plot.FIGURE_WIDTH, Config.Plot.FIGURE_HEIGHT)

# Configurações de precisão (use Config.Estatistica.*)
DECIMAL_PLACES = Config.Estatistica.PRECISAO_DECIMAL
R_SQUARED_THRESHOLD_EXCELLENT = Config.Estatistica.R2_EXCELENTE
R_SQUARED_THRESHOLD_GOOD = Config.Estatistica.R2_BOM
R_SQUARED_THRESHOLD_MODERATE = Config.Estatistica.R2_MODERADO
