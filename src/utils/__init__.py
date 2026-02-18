"""
Modulo de Utilidades

Contem funcoes auxiliares e validadores.
"""

from .parsers import eh_erro_instrumental, extrair_prefixo
from .validador import ValidadorDados

__all__ = [
    'eh_erro_instrumental',
    'extrair_prefixo',
    'ValidadorDados'
]