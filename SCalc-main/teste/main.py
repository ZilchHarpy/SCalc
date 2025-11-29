from src.utils import *

def main():
    print("Digite a quantidade de pontos: ")
    n = int(input())

    pontos = []
    for i in range(n):
        print(f"Digite o ponto {i + 1} (formato: x, y): ")
        ponto = tuple(map(float, input().split(',')))
        pontos.append(ponto)
    
    print("Digite o erro em x para cada ponto (formato: ex1, ex2, ..., exn): ")
    erros_x = list(map(float, input().split(',')))
    print("Digite o erro em y para cada ponto (formato: ey1, ey2, ..., eyn): ")
    erros_y = list(map(float, input().split(',')))

    PlotarGrafico(pontos, erros_x, erros_y)

if __name__ == "__main__":
    main()