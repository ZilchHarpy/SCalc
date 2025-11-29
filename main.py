from src.utils import *
import pandas as pd
'''
Funções usadas de utils:
- calcular_media(lista)
- calcular_desvio_padrao(lista)
- calcular_erro_estatistico(lista)
- calcular_erro_total(lista, erro_sistematico)
- LinLog(t, y)
- PlotarGrafico(pontos, erros_x, erros_y)
'''

if __name__ == "__main__":

    path = "src/data/ExFISMEC_MRU.xlsx"

    # Leitura dos dados do arquivo Excel
    dados_excel = pd.read_excel(path)

    # mostrar tabela
    print(dados_excel)

    # lista float para armazenar os tempos médios
    tempos = []

    # Calcular tempo medio das colunas t1, t2, t3 e calcular erro associado
    for index, row in dados_excel.iterrows():
        # se contiver elementos NaN, pular o c
        if(pd.isna(row['t1']) or pd.isna(row['t2']) or pd.isna(row['t3'])):
            continue
        else:
            t1 = float(row['t1'])
            t2 = float(row['t2'])
            t3 = float(row['t3'])
            media_tempo = calcular_media([t1, t2, t3])
            tempos.append(media_tempo)

    # Calcular erro estatístico e total dos tempos com base na coluna terr_instr
    erro_instr = float(dados_excel['terr_instr'][0])  # assumindo que o erro instrumental é o mesmo para todas as medições
    erro_estatistico_tempos = calcular_erro_estatistico(tempos)
    erro_total_tempos = calcular_erro_total(tempos, erro_instr)


    # Escrever tempos médios, tempos totais e erros na tabela4
    dados_excel['t_medio'] = pd.Series(tempos)
    dados_excel['terr_est'] = erro_estatistico_tempos
    dados_excel['terr_total'] = erro_total_tempos

    #print(f"tempos medios: {tempos}")
    #print(f"Erro estatístico dos tempos: {erro_estatistico_tempos:.4f}")
    #print(f"Erro total dos tempos: {erro_total_tempos:.4f}")

    print("\nTabela com tempos médios e erros:")
    print(dados_excel)

    



    '''
    # Entrada de dados pelo usuário
    dados = [float(x) for x in input("Digite os dados separados por vírgula: ").replace(" ", "").split(",")]
    erro_sistematico = float(input("Digite o erro sistemático: "))

    Imprime para o usuario uma tabela com os resultados no seguinte formato:
    Xi +/- Erro Sistematico
    ...
    Xn +/- Erro Sistematico

    Valor médio: j
    Erro Estatístico: k
    Erro Total: m
    print("\nResultados (mm):")
    for valor in dados:
        print(f"{valor:.2f} +/- {erro_sistematico:.4f}")
    
    erro_estatistico = calcular_erro_estatistico(dados)
    erro_total = calcular_erro_total(dados, erro_sistematico)   

    print(f"\nValor médio: {calcular_media(dados):.4f}")
    print(f"Erro Estatístico: {erro_estatistico:.4f}")
    print(f"Erro Total: {erro_total:.4f}")
    '''