"""
Módulo core - Contém a lógica principal de cálculos estatísticos e regressão
"""

from .statistics import calcular_estatisticas, particionar
from .regression import RegLin

__all__ = ['calcular_estatisticas', 'particionar', 'RegLin']
