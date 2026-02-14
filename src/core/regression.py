"""
Modulo de Regressao Linear

Contem funcoes para realizar analise de regressao linear
e calcular parametros estatisticos da reta.
"""

from scipy.stats import linregress
from typing import Tuple, List


def RegLin(x: List[float], y: List[float]) -> Tuple[float, float, float]:
    """
    Realiza a regressao linear dos dados usando scipy.stats.linregress.
    
    Calcula o coeficiente angular, linear e o coeficiente de determinacao (R2).
    
    Args:
        x (List[float]): Lista de valores independentes
        y (List[float]): Lista de valores dependentes
        
    Returns:
        Tuple[float, float, float]: 
            - slope: coeficiente angular (m)
            - intercept: coeficiente linear (b)
            - r_squared: coeficiente de determinacao (R2)
            
    Notes:
        A equacao da reta e: y = slope * x + intercept
        R2 indica o quao bem a reta se ajusta aos dados (0 a 1)
    """
    
    slope, intercept, r_value, p_value, std_err = linregress(x, y)

    # Retorna slope, intercept e R2 (r_value2)
    return slope, intercept, r_value ** 2
