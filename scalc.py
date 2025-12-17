from src.utils import Calcular_Estatisticas
from src.utils import RegLin
from src.utils import PlotarGrafico
import pandas as pd
import numpy as np

if __name__ == "__main__":

    # Definições iniciais
    path = "src/data/TBTeste.xlsx"
    ax_x = "log(t) [s]"
    ax_y = "log(d) [mm]"

    # Leitura dos dados do arquivo Excel
    dados_excel = pd.read_excel(path)

    # Cálculo das estatísticas
    medias, err_est, err_instr = Calcular_Estatisticas(dados_excel)

    # Preparação dos dados para regressão linear
    y, x = np.array(list(medias.values())[0]), np.array(list(medias.values())[1])
    y_err, x_err = np.array(list(err_est.values())[0]), np.array(list(err_est.values())[1])

    # Realiza a regressão linear
    slope, intercept, r_squared = RegLin(x, y)

    PlotarGrafico(set(zip(x, y)), x_err.tolist(), y_err.tolist(),
                    slope=slope,
                    intercept=intercept,
                    str_x=ax_x,
                    str_y=ax_y,
                    titulo="Gráfico de Dispersão com Regressão Linear") 

    # Adicionar opções:
    # 1. Gerar nova planilha
    # 2. Editar dados na planilha existente
    # 3. Sair sem fazer nada