"""
Excecoes customizadas SCalc
"""

class ScalcException(Exception):
    """Excecao base para todas as excecoes do SCalc"""
    pass


class DadosInvalidosException(ScalcException):
    """Excecao para dados invalidos ou mal formatados"""
    pass


class DadosInsuficientesException(ScalcException):
    """Excecao para dados insuficientes para analise"""
    pass


class ColunasInvalidasException(ScalcException):
    """Excecao para problemas com colunas do DataFrame"""
    pass


class DadosNaoNumericosException(ScalcException):
    """Excecao quando dados esperados nao sao numericos"""
    pass


class RegressaoException(ScalcException):
    """Excecao em calculos de regressao linear"""
    pass


class ArquivoInvalidoException(ScalcException):
    """Excecao para arquivos invalidos ou inacessiveis"""
    pass


class ConfiguracaoException(ScalcException):
    """Excecao para problemas de configuracao"""
    pass