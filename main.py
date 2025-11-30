from src.utils import calcular_media
from src.utils import calcular_erro_estatistico
from src.utils import calcular_erro_total
from src.utils import LinLog
from src.utils import PlotarGrafico

import pandas as pd

if __name__ == "__main__":

    path = "src/data/TBTeste.xlsx"

    # Leitura dos dados do arquivo Excel
    dados_excel = pd.read_excel(path)

    # Inicializar listas e constantes para armazenar os tempos médios e erros
    t_medio = []
    terr_est = []
    terr_total = []
    erro_instrumental = float(dados_excel['terr_instr'][0])  # assumindo que o erro instrumental é o mesmo para todas as medições

    # Calcular tempo medio das colunas t1, t2, t3 e calcular erro associado
    for index, row in dados_excel.iterrows():
        # se contiver elementos NaN, pular o ciclo
        if(pd.isna(row['t1']) or pd.isna(row['t2']) or pd.isna(row['t3'])):
            continue
        else:
            t1 = float(row['t1'])
            t2 = float(row['t2'])
            t3 = float(row['t3'])

            media_tempo = calcular_media([t1, t2, t3])
            erro_estatistico_tempo = calcular_erro_estatistico([t1, t2, t3])
            erro_total_tempo = calcular_erro_total([t1, t2, t3], erro_instrumental)

            # Armazenar os resultados nas listas
            t_medio.append(media_tempo)
            terr_est.append(erro_estatistico_tempo)
            terr_total.append(erro_total_tempo)


    # Escrever tempos médios, tempos totais e erros na tabela, com 4 casas decimais
    dados_excel.loc[:len(t_medio)-1, 't_medio'] = [round(val, 4) for val in t_medio]
    dados_excel.loc[:len(terr_est)-1, 'terr_est'] = [round(val, 4) for val in terr_est]
    dados_excel.loc[:len(terr_total)-1, 'terr_total'] = [round(val, 4) for val in terr_total]

    #print("\nTabela com tempos médios e erros:")
    #print(dados_excel)

    # Salvar a tabela atualizada em um novo arquivo Excel
    dados_excel.to_excel(path, index=False)


    # Preparar dados para plotagem
    # linearização logarítmica dos dados
    t_log, d_log, k, ln_b = LinLog(t_medio, dados_excel['d'][:len(t_medio)].tolist())

    # calcular erros logarítmicos no estilo k +/- kerr
    terr_log = [terr / t for terr, t in zip(terr_total, t_medio)]
    derr_log = [derr / d for derr, d in zip(dados_excel['derr'][:len(t_medio)].tolist(), dados_excel['d'][:len(t_medio)].tolist())]

    # preparar pontos para plotagem
    pontos = list(zip(t_log, d_log))
    erros_x = terr_log
    erros_y = derr_log

    # plotar gráfico com barras de erro
    #PlotarGrafico(pontos, erros_x, erros_y, k, ln_b)
    print(f"\nCoeficiente angular (k): {k}")
    print(f"Coeficiente linear (ln(b)): {ln_b}")
    