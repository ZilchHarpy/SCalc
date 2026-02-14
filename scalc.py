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
import logging
from pathlib import Path

import pandas as pd
import numpy as np

from src.data.config import Config, setup_logging
from src.core import calcular_estatisticas, RegLin
from src.visualization.plots import PlotarGrafico
from src.utils import ValidadorDados
from src.core.exceptions import (
    DadosInvalidosException,
    ArquivoInvalidoException,
    RegressaoException
)

# Configurar logger
logger = logging.getLogger(__name__)


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
    logger.info("="*60)
    logger.info("SCalc - Modo Linha de Comando")
    logger.info("="*60)
    
    try:
        # Validar arquivo
        logger.info(f"Validando arquivo: {path}")
        ValidadorDados.validar_arquivo_excel(path)
        
        # Leitura dos dados do arquivo Excel
        logger.info(f"Carregando arquivo: {path}")
        dados_excel = pd.read_excel(path)
        
        # Validar DataFrame
        logger.info(f"Validando DataFrame")
        ValidadorDados.validar_dataframe(dados_excel, "Dados do Excel")
        ValidadorDados.validar_tamanho_arquivo(dados_excel)
        
        logger.info(f"Arquivo carregado com sucesso: {len(dados_excel)} linhas, {len(dados_excel.columns)} colunas")
        
        # Cálculo das estatísticas
        logger.info("Calculando estatísticas...")
        resultado_stats = calcular_estatisticas(dados_excel)
        logger.info(f"Estatísticas calculadas para {len(resultado_stats)} variáveis")
        
        # Extrair dados das estatísticas
        medias = dict(zip(resultado_stats['Dados'], resultado_stats['Média']))
        err_est = dict(zip(resultado_stats['Dados'], resultado_stats['S_err']))
        err_total = dict(zip(resultado_stats['Dados'], resultado_stats['T_err']))
        
        logger.info(f"Variáveis encontradas: {', '.join(medias.keys())}")
        
        # Validar dados suficientes para regressão
        if len(medias) < 2:
            raise DadosInvalidosException("Mínimo de 2 variáveis necessário para regressão linear")
        
        # Preparação dos dados para regressão linear
        logger.info("Preparando dados para regressão linear...")
        dados_keys = list(medias.keys())
        x = np.array([medias[dados_keys[0]]])
        y = np.array([medias[dados_keys[1]]])
        x_err = np.array([err_est[dados_keys[0]]])
        y_err = np.array([err_est[dados_keys[1]]])
        
        # Realiza a regressão linear
        logger.info("Calculando regressão linear...")
        try:
            slope, intercept, r_squared = RegLin(x.tolist(), y.tolist())
        except Exception as e:
            raise RegressaoException(f"Erro na regressão linear: {str(e)}")
        
        # Mostrar resultados
        logger.info("="*60)
        logger.info("RESULTADOS DA REGRESSÃO LINEAR")
        logger.info("="*60)
        logger.info(f"Equação: y = {slope:.6f}x + {intercept:.6f}")
        logger.info(f"Coeficiente Angular (m): {slope:.6f}")
        logger.info(f"Coeficiente Linear (b): {intercept:.6f}")
        logger.info(f"R² (Coeficiente de Determinação): {r_squared:.6f}")
        
        # Classificar qualidade do ajuste
        qualidade = Config.validar_r2(r_squared)
        logger.info(f"Qualidade do ajuste: {qualidade}")
        
        logger.info("Plotando gráfico...")
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
        
        logger.info("Processo concluído com sucesso!")
        
    except ArquivoInvalidoException as e:
        logger.error(f"Erro de arquivo: {str(e)}")
        sys.exit(1)
    except DadosInvalidosException as e:
        logger.error(f"Erro nos dados: {str(e)}")
        sys.exit(1)
    except RegressaoException as e:
        logger.error(f"Erro na regressão: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Erro inesperado durante o processamento: {str(e)}")
        sys.exit(1)



def modo_gui():
    """
    Executa o programa em modo interface gráfica (GUI)
    """
    logger.info("Iniciando interface gráfica...")
    try:
        from src.visualization.gui import iniciar_interface
        iniciar_interface()
    except Exception as e:
        logger.exception(f"Erro ao iniciar interface gráfica: {str(e)}")
        sys.exit(1)


def main():
    """
    Função principal que decide qual modo executar
    """
    # Configurar logging
    from src.data.config import setup_logging
    setup_logging(nivel='INFO')
    
    parser = argparse.ArgumentParser(
        description=f'{Config.APP_NAME} - {Config.APP_DESCRIPTION}',
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
    
    logger.info(f"SCalc versão {Config.APP_VERSION} iniciado")
    
    # Decidir qual modo executar
    if args.cli:
        # Modo CLI
        if not args.arquivo:
            logger.error("No modo CLI, o argumento --arquivo é obrigatório!")
            parser.print_help()
            sys.exit(1)
        
        logger.info(f"Executando em modo CLI com arquivo: {args.arquivo}")
        modo_cli(
            path=args.arquivo,
            ax_x=args.x_label,
            ax_y=args.y_label,
            titulo=args.titulo
        )
    else:
        # Modo GUI (padrão)
        logger.info("Executando em modo GUI")
        modo_gui()


if __name__ == "__main__":
    main()
