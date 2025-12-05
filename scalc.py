from src.utils import *

import pandas as pd

if __name__ == "__main__":

    path = "src/data/TBTeste.xlsx"

    # Leitura dos dados do arquivo Excel
    dados_excel = pd.read_excel(path)

    print(dados_excel)