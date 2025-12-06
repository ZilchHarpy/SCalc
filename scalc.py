from src.utils import Calcular_Estatisticas
from src.utils import RegLin

import pandas as pd

if __name__ == "__main__":

    path = "src/data/TBTeste.xlsx"

    # Leitura dos dados do arquivo Excel
    dados_excel = pd.read_excel(path)

    print(dados_excel)

    medias, err_est, err_instr = Calcular_Estatisticas(dados_excel)
    pontos = RegLin(medias)

    # Adicionar opções:
    # 1. Gerar nova planilha
    # 2. Adicionar dados na planilha atual
    # 3. Sair