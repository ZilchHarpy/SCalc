"""
SCalc - Sistema de Calculo e Analise de Regressao Linear

Pode ser executado de duas formas:
  python scalc.py              # Modo GUI (padrao)
  python scalc.py --gui        # Modo GUI (explicito)
  python scalc.py --cli -f <arquivo.xlsx>  # Modo CLI

Autor: Caio Aquilino Merino
"""

import sys
import argparse
import logging
from pathlib import Path

import numpy as np
import pandas as pd

from src.data.config import Config, setup_logging
from src.core import calcular_estatisticas, calcular_stats_prefixo, RegLin
from src.core.statistics import particionar
from src.core.exceptions import (
    DadosInvalidosException,
    ArquivoInvalidoException,
    RegressaoException,
)
from src.utils.validador import ValidadorDados   # importado direto para evitar circular import
from src.visualization.plots import PlotarGrafico

logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------- #
#  Modo CLI                                                                    #
# --------------------------------------------------------------------------- #

def modo_cli(
    path: str,
    ax_x: str = "x",
    ax_y: str = "y",
    titulo: str = "Grafico de Dispersao com Regressao Linear",
) -> None:
    """
    Executa o programa em modo linha de comando.

    Carrega o arquivo Excel, executa o pipeline completo (particionar ->
    calcular_stats_prefixo -> RegLin -> PlotarGrafico) e imprime os
    resultados no terminal via logger.

    Args:
        path:   Caminho para o arquivo Excel.
        ax_x:   Rotulo do eixo X no grafico.
        ax_y:   Rotulo do eixo Y no grafico.
        titulo: Titulo do grafico.
    """
    logger.info("=" * 60)
    logger.info("SCalc - Modo Linha de Comando")
    logger.info("=" * 60)

    try:
        # ---------------------------------------------------------------- #
        #  Carregar e validar                                               #
        # ---------------------------------------------------------------- #
        logger.info(f"Validando arquivo: {path}")
        ValidadorDados.validar_arquivo_excel(path)

        logger.info(f"Carregando arquivo: {path}")
        dados_excel = pd.read_excel(path)

        ValidadorDados.validar_dataframe(dados_excel, "Dados do Excel")
        ValidadorDados.validar_tamanho_arquivo(dados_excel)
        logger.info(
            f"Arquivo carregado: {len(dados_excel)} linhas, "
            f"{len(dados_excel.columns)} colunas"
        )

        # ---------------------------------------------------------------- #
        #  Particionar                                                       #
        # ---------------------------------------------------------------- #
        logger.info("Particionando dados...")
        dados_brutos, erros_instr, _ = particionar(dados_excel)

        prefixos = sorted(dados_brutos.keys())
        logger.info(f"Grupos encontrados: {prefixos}")

        if len(prefixos) < 2:
            raise DadosInvalidosException(
                "Minimo de 2 grupos necessario para regressao linear"
            )

        prefixo_x, prefixo_y = prefixos[0], prefixos[1]
        logger.info(
            f"Regressao: '{prefixo_x}' (X) vs '{prefixo_y}' (Y)"
        )

        # ---------------------------------------------------------------- #
        #  Calcular medias e erros via helper centralizado                  #
        # ---------------------------------------------------------------- #
        x_vals, x_errs = calcular_stats_prefixo(
            dados_brutos[prefixo_x], erros_instr[prefixo_x]
        )
        y_vals, y_errs = calcular_stats_prefixo(
            dados_brutos[prefixo_y], erros_instr[prefixo_y]
        )

        if len(x_vals) < 2 or len(y_vals) < 2:
            raise DadosInvalidosException(
                "Dados insuficientes para regressao linear "
                "(minimo 2 pontos por grupo)"
            )
        if len(x_vals) != len(y_vals):
            raise DadosInvalidosException(
                f"Grupos com tamanhos diferentes: "
                f"{prefixo_x}={len(x_vals)}, {prefixo_y}={len(y_vals)}"
            )

        x = np.array(x_vals)
        y = np.array(y_vals)
        x_err = np.array(x_errs)
        y_err = np.array(y_errs)

        # ---------------------------------------------------------------- #
        #  Regressao linear                                                 #
        # ---------------------------------------------------------------- #
        logger.info("Calculando regressao linear...")
        try:
            slope, intercept, r_squared = RegLin(x.tolist(), y.tolist())
        except Exception as e:
            raise RegressaoException(f"Erro na regressao linear: {e}") from e

        qualidade = Config.validar_r2(r_squared)

        logger.info("=" * 60)
        logger.info("RESULTADOS DA REGRESSAO LINEAR")
        logger.info("=" * 60)
        logger.info(f"Grupo X : '{prefixo_x}' ({len(x)} pontos)")
        logger.info(f"Grupo Y : '{prefixo_y}' ({len(y)} pontos)")
        logger.info(f"Equacao : y = {slope:.6f}x + {intercept:.6f}")
        logger.info(f"m (angular)  : {slope:.6f}")
        logger.info(f"b (linear)   : {intercept:.6f}")
        logger.info(f"R2           : {r_squared:.6f}")
        logger.info(f"Qualidade    : {qualidade}")

        # ---------------------------------------------------------------- #
        #  Plotar                                                            #
        # ---------------------------------------------------------------- #
        logger.info("Plotando grafico...")
        PlotarGrafico(
            set(zip(x.tolist(), y.tolist())),
            x_err.tolist(),
            y_err.tolist(),
            slope=slope,
            intercept=intercept,
            str_x=ax_x,
            str_y=ax_y,
            titulo=titulo,
        )
        logger.info("Processo concluido com sucesso!")

    except ArquivoInvalidoException as e:
        logger.error(f"Erro de arquivo: {e}")
        sys.exit(1)
    except DadosInvalidosException as e:
        logger.error(f"Erro nos dados: {e}")
        sys.exit(1)
    except RegressaoException as e:
        logger.error(f"Erro na regressao: {e}")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Erro inesperado: {e}")
        sys.exit(1)


# --------------------------------------------------------------------------- #
#  Modo GUI                                                                    #
# --------------------------------------------------------------------------- #

def modo_gui() -> None:
    """Inicia a interface grafica."""
    logger.info("Iniciando interface grafica...")
    try:
        from src.visualization.gui import iniciar_interface
        iniciar_interface()
    except Exception as e:
        logger.exception(f"Erro ao iniciar interface grafica: {e}")
        sys.exit(1)


# --------------------------------------------------------------------------- #
#  Ponto de entrada                                                            #
# --------------------------------------------------------------------------- #

def main() -> None:
    setup_logging(nivel='INFO')

    parser = argparse.ArgumentParser(
        description=f"{Config.APP_NAME} - {Config.APP_DESCRIPTION}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:

  # Interface grafica (padrao):
  python scalc.py
  python scalc.py --gui

  # Linha de comando:
  python scalc.py --cli --arquivo dados.xlsx
  python scalc.py --cli -f dados.xlsx --x-label "Tempo (s)" --y-label "Distancia (m)"
        """,
    )

    parser.add_argument('--gui',  action='store_true',
                        help='Modo interface grafica (padrao)')
    parser.add_argument('--cli',  action='store_true',
                        help='Modo linha de comando')
    parser.add_argument('--arquivo', '-f', type=str,
                        help='Caminho para o arquivo Excel (obrigatorio no modo CLI)')
    parser.add_argument('--x-label', type=str, default='x',
                        help='Rotulo do eixo X (padrao: "x")')
    parser.add_argument('--y-label', type=str, default='y',
                        help='Rotulo do eixo Y (padrao: "y")')
    parser.add_argument('--titulo', type=str,
                        default='Grafico de Dispersao com Regressao Linear',
                        help='Titulo do grafico')

    args = parser.parse_args()
    logger.info(f"SCalc {Config.APP_VERSION} iniciado")

    if args.cli:
        if not args.arquivo:
            logger.error("Modo CLI requer --arquivo/-f")
            parser.print_help()
            sys.exit(1)
        modo_cli(
            path=args.arquivo,
            ax_x=args.x_label,
            ax_y=args.y_label,
            titulo=args.titulo,
        )
    else:
        modo_gui()


if __name__ == "__main__":
    main()
