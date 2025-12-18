"""
SCalc - Sistema de Cálculo e Análise de Regressão Linear

Módulo principal do SCalc. Expõe as principais funções para fácil acesso.
"""

from src.core import Calcular_Estatisticas, RegLin, Particionar
from src.visualization import PlotarGrafico

__version__ = '1.0.0'
__author__ = 'SCalc Team'

__all__ = [
    'Calcular_Estatisticas',
    'RegLin',
    'Particionar',
    'PlotarGrafico',
]
