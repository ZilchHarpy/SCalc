"""
SCalc - Sistema de Calculo e Analise de Regressao Linear

Este modulo pode ser executado de duas formas:
1. Modo CLI (linha de comando) - para processamento direto de arquivos
2. Modo GUI (interface grafica) - para uso interativo

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
from src.core.statistics import particionar
from src.visualization.plots import PlotarGrafico
from src.utils import ValidadorDados
from src.core.exceptions import (
    DadosInvalidosException,
    ArquivoInvalidoException,
    RegressaoException
)

# Configurar logger
logger = logging.getLogger(__name__)


def modo_cli(path: str, ax_x: str = "x", ax_y: str = "y", 
             titulo: str = "Grafico de Dispersao com Regressao Linear"):
    """
    Executa o programa em modo linha de comando (CLI)
    
    Args:
        path: Caminho para o arquivo Excel
        ax_x: Label do eixo X
        ax_y: Label do eixo Y
        titulo: Titulo do grafico
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
        
        # Obter dados brutos usando particionar
        logger.info("Particionando dados...")
        dados_brutos, erros_instr, dados_keys = particionar(dados_excel)
        
        # Obter prefixos (grupos)
        prefixos = sorted(dados_brutos.keys())
        
        logger.info(f"Prefixos encontrados: {prefixos}")
        
        if len(prefixos) < 2:
            raise DadosInvalidosException("Minimo de 2 grupos (prefixos) necessario para regressao linear")
        
        # Usar os dois primeiros prefixos para regressao
        prefixo_x = prefixos[0]
        prefixo_y = prefixos[1]
        
        logger.info(f"Realizando regressao linear entre '{prefixo_x}' (X) e '{prefixo_y}' (Y)...")
        
        # Calcular médias por iteração (a_1, a_2, a_3, etc)
        x = []
        y = []
        x_err = []
        y_err = []
        
        # Processar variável X - calcular média de cada iteração
        chaves_x = sorted(dados_brutos[prefixo_x].keys())
        for chave in chaves_x:
            valores = dados_brutos[prefixo_x][chave]
            if valores:
                media = sum(valores) / len(valores)
                x.append(media)
                
                # Calcular erro estatístico
                if len(valores) > 1:
                    desvio = (sum([(v - media) ** 2 for v in valores]) / (len(valores) - 1)) ** 0.5
                    erro_est = desvio / (len(valores) ** 0.5)
                else:
                    erro_est = 0.0
                
                # Obter erro instrumental
                erro_inst = erros_instr[prefixo_x][chave]
                
                # Calcular erro total
                erro_total = (erro_est ** 2 + erro_inst ** 2) ** 0.5
                x_err.append(erro_total)
        
        # Processar variável Y - calcular média de cada iteração
        chaves_y = sorted(dados_brutos[prefixo_y].keys())
        for chave in chaves_y:
            valores = dados_brutos[prefixo_y][chave]
            if valores:
                media = sum(valores) / len(valores)
                y.append(media)
                
                # Calcular erro estatístico
                if len(valores) > 1:
                    desvio = (sum([(v - media) ** 2 for v in valores]) / (len(valores) - 1)) ** 0.5
                    erro_est = desvio / (len(valores) ** 0.5)
                else:
                    erro_est = 0.0
                
                # Obter erro instrumental
                erro_inst = erros_instr[prefixo_y][chave]
                
                # Calcular erro total
                erro_total = (erro_est ** 2 + erro_inst ** 2) ** 0.5
                y_err.append(erro_total)
        
        # Validar dados suficientes
        if len(x) < 2 or len(y) < 2:
            raise DadosInvalidosException("Dados insuficientes para regressao linear (minimo 2 iteracoes por grupo)")
        
        if len(x) != len(y):
            raise DadosInvalidosException(f"Grupos com tamanhos diferentes: {prefixo_x}={len(x)}, {prefixo_y}={len(y)}")
        
        x = np.array(x)
        y = np.array(y)
        x_err = np.array(x_err)
        y_err = np.array(y_err)
        
        # Realiza a regressao linear
        logger.info("Calculando regressao linear...")
        try:
            slope, intercept, r_squared = RegLin(x.tolist(), y.tolist())
        except Exception as e:
            raise RegressaoException(f"Erro na regressao linear: {str(e)}")
        
        # Mostrar resultados
        logger.info("="*60)
        logger.info("RESULTADOS DA REGRESSAO LINEAR")
        logger.info("="*60)
        logger.info(f"Grupo X: '{prefixo_x}' com {len(x)} iteracoes")
        logger.info(f"Grupo Y: '{prefixo_y}' com {len(y)} iteracoes")
        logger.info(f"Equacao: y = {slope:.6f}x + {intercept:.6f}")
        logger.info(f"Coeficiente Angular (m): {slope:.6f}")
        logger.info(f"Coeficiente Linear (b): {intercept:.6f}")
        logger.info(f"R2 (Coeficiente de Determinacao): {r_squared:.6f}")
        
        # Classificar qualidade do ajuste
        if r_squared > 0.95:
            qualidade = "Excelente (R2 > 0.95)"
        elif r_squared > 0.85:
            qualidade = "Bom (R2 > 0.85)"
        elif r_squared > 0.70:
            qualidade = "Moderado (R2 > 0.70)"
        else:
            qualidade = "Fraco (R2 < 0.70)"
        
        logger.info(f"Qualidade do ajuste: {qualidade}")
        
        logger.info("Plotando grafico...")
        # Plotar grafico
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
        
        logger.info("Processo concluido com sucesso!")
        
    except ArquivoInvalidoException as e:
        logger.error(f"Erro de arquivo: {str(e)}")
        sys.exit(1)
    except DadosInvalidosException as e:
        logger.error(f"Erro nos dados: {str(e)}")
        sys.exit(1)
    except RegressaoException as e:
        logger.error(f"Erro na regressao: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Erro inesperado durante o processamento: {str(e)}")
        sys.exit(1)



def modo_gui():
    """
    Executa o programa em modo interface grafica (GUI)
    """
    logger.info("Iniciando interface grafica...")
    try:
        from src.visualization.gui import iniciar_interface
        iniciar_interface()
    except Exception as e:
        logger.exception(f"Erro ao iniciar interface grafica: {str(e)}")
        sys.exit(1)


def main():
    """
    Funcao principal que decide qual modo executar
    """
    # Configurar logging
    from src.data.config import setup_logging
    setup_logging(nivel='INFO')
    
    parser = argparse.ArgumentParser(
        description=f'{Config.APP_NAME} - {Config.APP_DESCRIPTION}',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Exemplos de uso:

  # Modo GUI (interface grafica):
  python scalc.py
  python scalc.py --gui

  # Modo CLI (linha de comando):
  python scalc.py --cli --arquivo src/data/TBTeste.xlsx
  python scalc.py --cli --arquivo dados.xlsx --x-label "Tempo (s)" --y-label "Distancia (m)"
        '''
    )
    
    parser.add_argument(
        '--gui',
        action='store_true',
        help='Executar em modo interface grafica (padrao se nenhum argumento for fornecido)'
    )
    
    parser.add_argument(
        '--cli',
        action='store_true',
        help='Executar em modo linha de comando'
    )
    
    parser.add_argument(
        '--arquivo', '-f',
        type=str,
        help='Caminho para o arquivo Excel (obrigatorio no modo CLI)'
    )
    
    parser.add_argument(
        '--x-label',
        type=str,
        default='x',
        help='Label do eixo X (padrao: "x")'
    )
    
    parser.add_argument(
        '--y-label',
        type=str,
        default='y',
        help='Label do eixo Y (padrao: "y")'
    )
    
    parser.add_argument(
        '--titulo',
        type=str,
        default='Grafico de Dispersao com Regressao Linear',
        help='Titulo do grafico'
    )
    
    args = parser.parse_args()
    
    logger.info(f"SCalc versao {Config.APP_VERSION} iniciado")
    
    # Decidir qual modo executar
    if args.cli:
        # Modo CLI
        if not args.arquivo:
            logger.error("No modo CLI, o argumento --arquivo e obrigatorio!")
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
        # Modo GUI (padrao)
        logger.info("Executando em modo GUI")
        modo_gui()


if __name__ == "__main__":
    main()
