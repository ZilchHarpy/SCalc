"""
Modulo de Regressao Linear

Contem funcoes para realizar analise de regressao linear
e calcular parametros estatisticos da reta.
"""

from scipy.stats import linregress
from typing import Tuple, List, Any
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
    x_array: Any = np.array(x, dtype=float)
    y_array: Any = np.array(y, dtype=float)
    
    # Realizar regressao linear
    # linregress retorna uma tupla: (slope, intercept, rvalue, pvalue, stderr)
    reg_result: Any = linregress(x_array, y_array)
    
    # Extrair valores usando indexacao (mais robusto para Pylance)
    slope: float = float(reg_result[0])      # Coeficiente angular
    intercept: float = float(reg_result[1])  # Coeficiente linear
    r_value: float = float(reg_result[2])    # Coeficiente de correlacao
    
    # Calcular R2 (coeficiente de determinacao)
    r_squared: float = r_value * r_value
    
    # Retornar slope, intercept e R2
    return slope, intercept, r_squared
