"""
Módulo core - Contém a lógica principal de cálculos estatísticos e regressão
"""

from .statistics import Calcular_Estatisticas, particionar
from .regression import RegLin

__all__ = ['Calcular_Estatisticas', 'Particionar', 'RegLin']
