"""
Módulo de Plotagem de Gráficos

Contém funções para visualização de dados e regressão linear.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Set
from src.data.config import Config


def PlotarGrafico(
    pontos: Set[Tuple[float, float]],
    erros_x: List[float],
    erros_y: List[float],
    str_x: str,
    slope: float,
    intercept: float,
    str_y: str,
    titulo: str
) -> None:
    """
    Plota um gráfico de dispersão com barras de erro e reta de regressão linear.
    
    Args:
        pontos: Conjunto de tuplas (x, y) dos pontos a plotar
        erros_x: Lista de erros para o eixo X
        erros_y: Lista de erros para o eixo Y
        str_x: Label do eixo X
        slope: Coeficiente angular da reta de regressão
        intercept: Coeficiente linear da reta de regressão
        str_y: Label do eixo Y
        titulo: Título do gráfico
        
    Returns:
        None (exibe o gráfico)
    """
    plt.style.use(Config.Plot.STYLE)

    x, y = zip(*pontos)

    # Criar o gráfico e plotar barras de erro
    fig, ax = plt.subplots(
        figsize=(Config.Plot.FIGURE_WIDTH, Config.Plot.FIGURE_HEIGHT),
        dpi=Config.Plot.FIGURE_DPI
    )
    ax.errorbar(
        x, y, 
        xerr=erros_x, 
        yerr=erros_y, 
        fmt='o',
        color=Config.Plot.COLOR_PONTOS,
        ecolor=Config.Plot.COLOR_ERRO,
        capsize=Config.Plot.CAPSIZE_ERRO
    )

    # Plotar a melhor reta
    x_fit = np.linspace(min(x) - 0.05 * min(x), max(x) + 0.05 * max(x), 500)
    y_fit = slope * x_fit + intercept
    arx_fit = [round(num) for num in x_fit]
    ary_fit = [round(num) for num in y_fit]
    ax.plot(x_fit, y_fit, color='blue', label='Melhor Reta')
    ax.legend()

    # Configurações do gráfico
    ax.set_title(titulo)
    ax.set_xlabel(str_x)
    ax.set_ylabel(str_y)
    ax.set(
        xlim=(min(arx_fit) - 0.05 * min(arx_fit), max(arx_fit) + 0.05 * max(arx_fit)),
        xticks=np.arange(min(arx_fit), max(arx_fit) + 1),
        ylim=(min(ary_fit) - 0.05 * max(ary_fit), max(ary_fit) + 0.05 * max(ary_fit)),
        yticks=np.arange(min(ary_fit), max(ary_fit) + 1),
    )

    plt.show()
