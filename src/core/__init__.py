"""
Modulo core - Contem a logica principal de calculos estatisticos e regressao.
"""

from .statistics import calcular_estatisticas, particionar, calcular_stats_prefixo
from .regression import RegLin

__all__ = [
    'calcular_estatisticas',
    'particionar',
    'calcular_stats_prefixo',
    'RegLin',
]
