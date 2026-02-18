"""
Modulo de Utilidades

Contem funcoes auxiliares e validadores.

Nota: ValidadorDados nao e exportado daqui para evitar importacao circular.
Importe diretamente de src.utils.validador quando necessario:
    from src.utils.validador import ValidadorDados
"""

from .parsers import eh_erro_instrumental, extrair_prefixo, contar

__all__ = [
    'eh_erro_instrumental',
    'extrair_prefixo',
    'contar',
]
