"""
Módulo core - Contém a lógica principal de cálculos estatísticos e regressão
"""

from .statistics import Calcular_Estatisticas, Particionar
from .regression import RegLin

__all__ = ['Calcular_Estatisticas', 'Particionar', 'RegLin']
