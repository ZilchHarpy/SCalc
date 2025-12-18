"""
Módulo de Configuração

Contém configurações globais e caminhos do projeto.
"""

import os

# Diretório base do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Diretórios principais
SRC_DIR = os.path.join(BASE_DIR, 'src')
DATA_DIR = os.path.join(BASE_DIR, 'src', 'data')
EXAMPLES_DIR = os.path.join(BASE_DIR, 'examples')
TESTS_DIR = os.path.join(BASE_DIR, 'tests')
DOCS_DIR = os.path.join(BASE_DIR, 'docs')

# Configurações da aplicação
APP_NAME = 'SCalc'
APP_VERSION = '1.0.0'
APP_DESCRIPTION = 'Sistema de Cálculo e Análise de Regressão Linear'

# Configurações de visualização
PLOT_STYLE = '_mpl-gallery'
PLOT_DPI = 100
PLOT_FIGURE_SIZE = (10, 8)

# Configurações de precisão
DECIMAL_PLACES = 6
R_SQUARED_THRESHOLD_EXCELLENT = 0.95
R_SQUARED_THRESHOLD_GOOD = 0.85
R_SQUARED_THRESHOLD_MODERATE = 0.70
