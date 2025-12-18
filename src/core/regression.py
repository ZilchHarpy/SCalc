"""
Módulo de Regressão Linear

Contém funções para realizar análise de regressão linear
e calcular parâmetros estatísticos da reta.
"""

from scipy.stats import linregress
from typing import Tuple, List


def RegLin(x: List[float], y: List[float]) -> Tuple[float, float, float]:
    """
    Realiza a regressão linear dos dados usando scipy.stats.linregress.
    
    Calcula o coeficiente angular, linear e o coeficiente de determinação (R²).
    
    Args:
        x (List[float]): Lista de valores independentes
        y (List[float]): Lista de valores dependentes
        
    Returns:
        Tuple[float, float, float]: 
            - slope: coeficiente angular (m)
            - intercept: coeficiente linear (b)
            - r_squared: coeficiente de determinação (R²)
            
    Notes:
        A equação da reta é: y = slope * x + intercept
        R² indica o quão bem a reta se ajusta aos dados (0 a 1)
    """
    
    slope, intercept, r_value, p_value, std_err = linregress(x, y)

    # Retorna slope, intercept e R² (r_value²)
    return slope, intercept, r_value ** 2
