"""
SCalc - Sistema de Calculo e Analise de Regressao Linear

Modulo principal do SCalc. Expoe as principais funcoes para facil acesso.
"""

from src.core import calcular_estatisticas, RegLin, particionar
from src.visualization import PlotarGrafico
from src.utils import eh_erro_instrumental

__version__ = '1.0.0'
__author__ = 'Caio A. Merino'

__all__ = [
    'calcular_estatisticas',
    'RegLin',
    'particionar',
    'PlotarGrafico',
    'eh_erro_instrumental'
]
