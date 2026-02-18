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
        
        # Calculo das estatisticas
        logger.info("Calculando estatisticas...")
        resultado_stats = calcular_estatisticas(dados_excel)
        logger.info(f"Estatisticas calculadas para {len(resultado_stats)} variaveis")
        
        # Extrair dados das estatisticas
        medias = dict(zip(resultado_stats['Dados'], resultado_stats['Media']))
        err_est = dict(zip(resultado_stats['Dados'], resultado_stats['S_err']))
        err_total = dict(zip(resultado_stats['Dados'], resultado_stats['T_err']))
        
        logger.info(f"Variaveis encontradas: {', '.join(medias.keys())}")
        
        # Validar dados suficientes para regressao
        if len(medias) < 2:
            raise DadosInvalidosException("Minimo de 2 variaveis necessario para regressao linear")
        
        # Preparacao dos dados para regressao linear
        logger.info("Preparando dados para regressao linear...")
        
        # Reorganizar dados por iteracao (1, 2, 3) para cada grupo (a, b, c)
        # Estrutura esperada: {'a': {'a_1': media, 'a_2': media, ...}, 'b': {...}, ...}
        dados_por_iteracao = {}
        
        for dado, media in medias.items():
            # Extrair prefixo (a, b, c) e numero (1, 2, 3)
            partes = dado.rsplit('_', 1)
            if len(partes) == 2:
                prefixo, numero = partes
                if numero not in dados_por_iteracao:
                    dados_por_iteracao[numero] = {}
                dados_por_iteracao[numero][prefixo] = {
                    'media': media,
                    'err_est': err_est[dado],
                    'err_total': err_total[dado]
                }
        
        # Obter lista de grupos (prefixos) e iteracoes
        grupos = sorted(set(prefixo for iterar in dados_por_iteracao.values() for prefixo in iterar.keys()))
        iteracoes = sorted(dados_por_iteracao.keys())
        
        logger.info(f"Grupos encontrados: {grupos}")
        logger.info(f"Iteracoes encontradas: {iteracoes}")
        
        if len(grupos) < 2:
            raise DadosInvalidosException("Minimo de 2 grupos necessario para regressao linear")
        
        if len(iteracoes) < 2:
            raise DadosInvalidosException("Minimo de 2 iteracoes necessario para regressao linear")
        
        # Fazer regressao entre primeiro e segundo grupo usando iteracoes como pontos
        grupo_x = grupos[0]
        grupo_y = grupos[1]
        
        x = []
        y = []
        x_err = []
        y_err = []
        
        for iteracao in iteracoes:
            if grupo_x in dados_por_iteracao[iteracao] and grupo_y in dados_por_iteracao[iteracao]:
                x.append(dados_por_iteracao[iteracao][grupo_x]['media'])
                y.append(dados_por_iteracao[iteracao][grupo_y]['media'])
                x_err.append(dados_por_iteracao[iteracao][grupo_x]['err_est'])
                y_err.append(dados_por_iteracao[iteracao][grupo_y]['err_est'])
        
        if len(x) < 2:
            raise DadosInvalidosException("Dados insuficientes para regressao linear")
        
        x = np.array(x)
        y = np.array(y)
        x_err = np.array(x_err)
        y_err = np.array(y_err)
        
        # Realiza a regressao linear
        logger.info(f"Calculando regressao linear entre grupos '{grupo_x}' e '{grupo_y}'...")
        try:
            slope, intercept, r_squared = RegLin(x.tolist(), y.tolist())
        except Exception as e:
            raise RegressaoException(f"Erro na regressao linear: {str(e)}")
        
        # Mostrar resultados
        logger.info("="*60)
        logger.info("RESULTADOS DA REGRESSAO LINEAR")
        logger.info("="*60)
        logger.info(f"Equacao: y = {slope:.6f}x + {intercept:.6f}")
        logger.info(f"Coeficiente Angular (m): {slope:.6f}")
        logger.info(f"Coeficiente Linear (b): {intercept:.6f}")
        logger.info(f"R2 (Coeficiente de Determinacao): {r_squared:.6f}")
        
        # Classificar qualidade do ajuste
        qualidade = Config.validar_r2(r_squared)
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
        default='log(t) [s]',
        help='Label do eixo X (padrao: "log(t) [s]")'
    )
    
    parser.add_argument(
        '--y-label',
        type=str,
        default='log(d) [mm]',
        help='Label do eixo Y (padrao: "log(d) [mm]")'
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
