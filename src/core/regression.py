"""
Modulo de Regressao Linear

Contem funcoes para realizar analise de regressao linear
e calcular parametros estatisticos da reta.
"""

from scipy.stats import linregress
from typing import Tuple, List
import numpy as np


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
    
    # Converter listas para arrays numpy (melhora performance e compatibilidade)
    x_array = np.array(x, dtype=float)
    y_array = np.array(y, dtype=float)
    
    # Realizar regressao linear
    # linregress retorna: LinregressResult ou tupla (slope, intercept, rvalue, pvalue, stderr)
    reg_result = linregress(x_array, y_array)
    
    # Acessar valores por indice
    # Indices: [0]=slope, [1]=intercept, [2]=rvalue, [3]=pvalue, [4]=stderr
    slope: float = float(reg_result[0])  # type: ignore
    intercept: float = float(reg_result[1])  # type: ignore
    r_value: float = float(reg_result[2])  # type: ignore
    
    # Calcular R2 (coeficiente de determinacao)
    r_squared: float = r_value * r_value
    
    # Retornar slope, intercept e R2
    return slope, intercept, r_squared