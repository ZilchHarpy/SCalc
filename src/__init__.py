"""
SCalc - Sistema de Cálculo e Análise de Regressão Linear

Módulo principal do SCalc. Expõe as principais funções para fácil acesso.
"""

from src.core import Calcular_Estatisticas, RegLin, particionar
from src.visualization import PlotarGrafico
from src.utils import eh_erro_instrumental

__version__ = '1.0.0'
__author__ = 'Caio A. Merino'

__all__ = [
    'Calcular_Estatisticas',
    'RegLin',
    'particionar',
    'PlotarGrafico',
]
