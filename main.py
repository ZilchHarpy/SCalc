from src.utils import *

if __name__ == "__main__":

    # Entrada de dados pelo usuário
    dados = [float(x) for x in input("Digite os dados separados por vírgula: ").replace(" ", "").split(",")]
    erro_sistematico = float(input("Digite o erro sistemático: "))

    ''' Imprime para o usuario uma tabela com os resultados no seguinte formato:
    Xi +/- Erro Sistematico
    ...
    Xn +/- Erro Sistematico

    Valor médio: j
    Erro Estatístico: k
    Erro Total: m
    '''
    print("\nResultados (mm):")
    for valor in dados:
        print(f"{valor:.2f} +/- {erro_sistematico:.2f}")
    
    erro_estatistico = calcular_erro_estatistico(dados)
    erro_total = calcular_erro_total(dados, erro_sistematico)   

    print(f"\nValor médio: {calcular_media(dados):.4f}")
    print(f"Erro Estatístico: {erro_estatistico:.4f}")
    print(f"Erro Total: {erro_total:.4f}")
