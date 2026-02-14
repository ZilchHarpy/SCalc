"""
Exceções customizadas SCalc
"""

class ScalcException(Exception):
    """Exceção base para todas as exceções do SCalc"""
    pass


class DadosInvalidosException(ScalcException):
    """Exceção para dados inválidos ou mal formatados"""
    pass


class DadosInsuficientesException(ScalcException):
    """Exceção para dados insuficientes para análise"""
    pass


class ColunasInvalidasException(ScalcException):
    """Exceção para problemas com colunas do DataFrame"""
    pass


class DadosNaoNumericosException(ScalcException):
    """Exceção quando dados esperados não são numéricos"""
    pass


class RegressaoException(ScalcException):
    """Exceção em cálculos de regressão linear"""
    pass


class ArquivoInvalidoException(ScalcException):
    """Exceção para arquivos inválidos ou inacessíveis"""
    pass


class ConfiguracaoException(ScalcException):
    """Exceção para problemas de configuração"""
    pass