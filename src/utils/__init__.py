"""
Módulo de Utilidades

Contém funções auxiliares e validadores.
"""

from .parsers import eh_erro_instrumental
from .validador import ValidadorDados

__all__ = [
    'eh_erro_instrumental',
    'ValidadorDados'
]