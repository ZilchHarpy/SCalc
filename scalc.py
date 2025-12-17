"""
SCalc - Sistema de Cálculo e Análise de Regressão Linear

Este módulo pode ser executado de duas formas:
1. Modo CLI (linha de comando) - para processamento direto de arquivos
2. Modo GUI (interface gráfica) - para uso interativo

Autor: [Seu Nome]
Data: 2025
"""

import sys
import argparse
from src.utils import Calcular_Estatisticas, RegLin, PlotarGrafico
import pandas as pd
import numpy as np


def modo_cli(path: str, ax_x: str = "log(t) [s]", ax_y: str = "log(d) [mm]", 
             titulo: str = "Gráfico de Dispersão com Regressão Linear"):
    """
    Executa o programa em modo linha de comando (CLI)
    
    Args:
        path: Caminho para o arquivo Excel
        ax_x: Label do eixo X
        ax_y: Label do eixo Y
        titulo: Título do gráfico
    """
    print("=" * 60)
    print("SCalc - Modo Linha de Comando")
    print("=" * 60)
    
    try:
        # Leitura dos dados do arquivo Excel
        print(f"\n📁 Carregando arquivo: {path}")
        dados_excel = pd.read_excel(path)
        print(f"✓ Arquivo carregado com sucesso!")
        print(f"  Linhas: {len(dados_excel)}")
        print(f"  Colunas: {len(dados_excel.columns)}")
        
        # Cálculo das estatísticas
        print("\n🔢 Calculando estatísticas...")
        medias, err_est, err_instr = Calcular_Estatisticas(dados_excel)
        print(f"✓ Estatísticas calculadas!")
        print(f"  Variáveis encontradas: {', '.join(medias.keys())}")
        
        # Preparação dos dados para regressão linear
        print("\n📊 Preparando dados para regressão linear...")
        y, x = np.array(list(medias.values())[0]), np.array(list(medias.values())[1])
        y_err, x_err = np.array(list(err_est.values())[0]), np.array(list(err_est.values())[1])
        
        # Realiza a regressão linear
        print("📈 Calculando regressão linear...")
        slope, intercept, r_squared = RegLin(x, y)
        
        # Mostrar resultados
        print("\n" + "=" * 60)
        print("RESULTADOS DA REGRESSÃO LINEAR")
        print("=" * 60)
        print(f"Equação: y = {slope:.6f}x + {intercept:.6f}")
        print(f"Coeficiente Angular (m): {slope:.6f}")
        print(f"Coeficiente Linear (b): {intercept:.6f}")
        print(f"R² (Coeficiente de Determinação): {r_squared:.6f}")
        
        if r_squared > 0.95:
            print("✓ Excelente ajuste (R² > 0.95)")
        elif r_squared > 0.85:
            print("✓ Bom ajuste (R² > 0.85)")
        elif r_squared > 0.70:
            print("⚠️ Ajuste moderado (R² > 0.70)")
        else:
            print("⚠️ Ajuste fraco (R² < 0.70)")
        
        print("\n🎨 Plotando gráfico...")
        # Plotar gráfico
        PlotarGrafico(
            set(zip(x, y)),
            x_err.tolist(),
            y_err.tolist(),
            slope=slope,
            intercept=intercept,
            str_x=ax_x,
            str_y=ax_y,
            titulo=titulo
        )
        
        print("✓ Processo concluído com sucesso!")
        
    except FileNotFoundError:
        print(f"❌ Erro: Arquivo não encontrado: {path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro durante o processamento: {str(e)}")
        sys.exit(1)


def modo_gui():
    """
    Executa o programa em modo interface gráfica (GUI)
    """
    from src.visualisation import iniciar_interface
    iniciar_interface()


def main():
    """
    Função principal que decide qual modo executar
    """
    parser = argparse.ArgumentParser(
        description='SCalc - Sistema de Cálculo e Análise de Regressão Linear',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Exemplos de uso:

  # Modo GUI (interface gráfica):
  python scalc.py
  python scalc.py --gui

  # Modo CLI (linha de comando):
  python scalc.py --cli --arquivo src/data/TBTeste.xlsx
  python scalc.py --cli --arquivo dados.xlsx --x-label "Tempo (s)" --y-label "Distância (m)"
        '''
    )
    
    parser.add_argument(
        '--gui',
        action='store_true',
        help='Executar em modo interface gráfica (padrão se nenhum argumento for fornecido)'
    )
    
    parser.add_argument(
        '--cli',
        action='store_true',
        help='Executar em modo linha de comando'
    )
    
    parser.add_argument(
        '--arquivo', '-f',
        type=str,
        help='Caminho para o arquivo Excel (obrigatório no modo CLI)'
    )
    
    parser.add_argument(
        '--x-label',
        type=str,
        default='log(t) [s]',
        help='Label do eixo X (padrão: "log(t) [s]")'
    )
    
    parser.add_argument(
        '--y-label',
        type=str,
        default='log(d) [mm]',
        help='Label do eixo Y (padrão: "log(d) [mm]")'
    )
    
    parser.add_argument(
        '--titulo',
        type=str,
        default='Gráfico de Dispersão com Regressão Linear',
        help='Título do gráfico'
    )
    
    args = parser.parse_args()
    
    # Decidir qual modo executar
    if args.cli:
        # Modo CLI
        if not args.arquivo:
            print("❌ Erro: No modo CLI, o argumento --arquivo é obrigatório!")
            parser.print_help()
            sys.exit(1)
        
        modo_cli(
            path=args.arquivo,
            ax_x=args.x_label,
            ax_y=args.y_label,
            titulo=args.titulo
        )
    else:
        # Modo GUI (padrão)
        modo_gui()


if __name__ == "__main__":
    main()
