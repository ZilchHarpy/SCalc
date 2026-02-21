#!/usr/bin/env python3
"""
Script de build do SCalc usando PyInstaller.

Uso:
    python build.py               # Build padrão (onefile, sem confirmação em CI)
    python build.py --onedir      # Build em modo diretório (inicialização mais rápida)
    python build.py --windowed    # Oculta o console (somente GUI, quebra o modo CLI)
    python build.py --no-clean    # Não remove builds anteriores
    python build.py -y            # Sem confirmação interativa
"""

import subprocess
import sys
import platform
import os
import shutil
from pathlib import Path
from datetime import datetime


class PyInstallerBuilder:
    """Gerenciador de build com PyInstaller."""

    def __init__(self):
        self.sistema = platform.system()
        self.arquitetura = platform.machine()
        self.python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        self.project_root = Path(__file__).parent
        self.dist_dir = self.project_root / "dist"
        self.build_dir = self.project_root / "build"

    # ------------------------------------------------------------------ #
    #  Verificação                                                         #
    # ------------------------------------------------------------------ #

    def verificar_pyinstaller(self) -> bool:
        """Verifica se o PyInstaller está instalado."""
        try:
            import PyInstaller  # noqa: F401
            versao = __import__("PyInstaller").__version__
            print(f"✓ PyInstaller {versao} encontrado")
            return True
        except ImportError:
            print("✗ PyInstaller não instalado.")
            print("  Instale com:  pip install pyinstaller")
            return False

    # ------------------------------------------------------------------ #
    #  Limpeza                                                             #
    # ------------------------------------------------------------------ #

    def limpar_builds_anteriores(self):
        """Remove artefatos de builds anteriores."""
        for alvo in ["build", "dist"]:
            path = self.project_root / alvo
            if path.exists():
                print(f"  Removendo {alvo}/")
                shutil.rmtree(path, ignore_errors=True)

        for spec in self.project_root.glob("*.spec"):
            print(f"  Removendo {spec.name}")
            spec.unlink()

    # ------------------------------------------------------------------ #
    #  Construção do comando                                               #
    # ------------------------------------------------------------------ #

    def _icone(self) -> Path | None:
        """Retorna o caminho do ícone adequado ao sistema operacional."""
        assets = self.project_root / "assets"
        if self.sistema == "Windows":
            candidate = assets / "scalc_icon.ico"
        elif self.sistema == "Darwin":
            candidate = assets / "scalc_icon.icns"
        else:
            return None

        return candidate if candidate.exists() else None

    def get_comando(self, modo: str, windowed: bool) -> list[str]:
        """
        Monta o comando PyInstaller completo.

        Args:
            modo: ``'onefile'`` ou ``'onedir'``.
            windowed: Se True, oculta o console no Windows/macOS.
                      ATENÇÃO: ocultar o console quebra o modo CLI.
        """
        cmd = [sys.executable, "-m", "PyInstaller"]

        # Modo de empacotamento
        cmd.append("--onefile" if modo == "onefile" else "--onedir")

        # Janela de console
        # --windowed oculta o console no Windows/macOS — útil para build
        # exclusivo de GUI. Para manter o modo CLI funcional, não usar.
        if windowed and self.sistema in ("Windows", "Darwin"):
            cmd.append("--windowed")

        # Caminhos de saída
        cmd += [
            "--name", "SCalc",
            "--distpath", str(self.dist_dir),
            "--workpath", str(self.build_dir),   # flag correta do PyInstaller
            "--specpath", str(self.project_root),
        ]

        # Hidden imports — pacotes que o PyInstaller não detecta
        # automaticamente por importação dinâmica ou sub-módulos.
        hidden_imports = [
            # numpy
            "numpy",
            "numpy.random",
            "numpy.core",
            "numpy.lib",
            # scipy: sub-módulos usados por linregress
            "scipy.stats",
            "scipy.stats._stats_py",
            "scipy.linalg",
            "scipy.optimize",
            "scipy._lib.messagestream",
            # pandas
            "pandas._libs.tslibs.np_datetime",
            "pandas._libs.tslibs.nattype",
            "pandas._libs.tslibs.timedeltas",
            "pandas._libs.tslibs.offsets",
            # openpyxl
            "openpyxl.styles",
            "openpyxl.utils",
            # matplotlib backend
            "matplotlib.backends.backend_qt5agg",
            "matplotlib.backends.backend_qtagg",
            # PySide6
            "PySide6.QtCore",
            "PySide6.QtGui",
            "PySide6.QtWidgets",
            # módulos internos do SCalc
            "src.core",
            "src.core.statistics",
            "src.core.regression",
            "src.core.exceptions",
            "src.visualization",
            "src.visualization.gui",
            "src.visualization.plots",
            "src.utils",
            "src.utils.parsers",
            "src.utils.validador",
            "src.data",
            "src.data.config",
        ]

        for imp in hidden_imports:
            cmd += ["--hidden-import", imp]

        # Dados extras (assets)
        assets = self.project_root / "assets"
        if assets.exists():
            sep = os.pathsep            # ';' no Windows, ':' no Unix
            cmd += ["--add-data", f"{assets}{sep}assets"]

        # Ícone
        icone = self._icone()
        if icone:
            cmd += ["--icon", str(icone)]

        # Otimização — nível 1 é seguro; nível 2 pode corromper docstrings
        # usadas por bibliotecas científicas (scipy, numpy).
        cmd += ["--optimize", "1"]

        # Ponto de entrada
        cmd.append("scalc.py")

        return cmd

    # ------------------------------------------------------------------ #
    #  Exibição                                                            #
    # ------------------------------------------------------------------ #

    def exibir_info(self, modo: str, windowed: bool):
        print(f"\n{'='*65}")
        print(f"  BUILD — SCalc  |  PyInstaller  |  {self.sistema} {self.arquitetura}")
        print(f"{'='*65}")
        print(f"  Python   : {self.python_version}")
        print(f"  Modo     : {modo.upper()}")
        print(f"  Windowed : {'SIM  ⚠ CLI ficará mudo' if windowed else 'NÃO  (CLI funcional)'}")
        print(f"  Saída    : {self.dist_dir}")

        estimativas = {
            "onefile": ("~150–250 MB", "3–6 min", "3–6 s"),
            "onedir":  ("~200–350 MB (pasta)", "1–3 min", "1–2 s"),
        }
        tam, tempo, init = estimativas[modo]
        print(f"\n  Tamanho estimado       : {tam}")
        print(f"  Tempo de build         : {tempo}")
        print(f"  Tempo de inicialização : {init}\n")

    # ------------------------------------------------------------------ #
    #  Execução                                                            #
    # ------------------------------------------------------------------ #

    def executar_build(self, modo: str, windowed: bool) -> int:
        """
        Executa o PyInstaller.

        Returns:
            0 em caso de sucesso, 1 em caso de falha.
        """
        cmd = self.get_comando(modo, windowed)

        print(f"Comando:\n  {' '.join(cmd)}\n")
        print("-" * 65)
        print("Aguarde… (pode levar alguns minutos)")
        print("-" * 65 + "\n")

        inicio = datetime.now()
        resultado = subprocess.run(cmd)
        duracao = datetime.now() - inicio

        if resultado.returncode == 0:
            self._exibir_sucesso(modo, duracao)
            return 0
        else:
            self._exibir_falha()
            return 1

    def _exibir_sucesso(self, modo: str, duracao):
        exe_nome = "SCalc.exe" if self.sistema == "Windows" else "SCalc"

        if modo == "onefile":
            exe_path = self.dist_dir / exe_nome
        else:
            exe_path = self.dist_dir / "SCalc" / exe_nome

        print(f"\n{'='*65}")
        print("  ✓ BUILD CONCLUÍDO COM SUCESSO!")
        print(f"{'='*65}")
        print(f"  Executável : {exe_path}")

        if exe_path.exists():
            tam_mb = exe_path.stat().st_size / (1024 ** 2)
            print(f"  Tamanho    : {tam_mb:.1f} MB")

        print(f"  Tempo      : {duracao}\n")
        print("Próximos passos:")
        print("  1. Teste o executável gerado")
        print("  2. Valide em uma máquina sem Python instalado")
        print("  3. Publique em GitHub Releases\n")

    def _exibir_falha(self):
        print(f"\n{'='*65}")
        print("  ✗ BUILD FALHOU")
        print(f"{'='*65}")
        print("\nVerifique os erros acima e tente:")
        print("  pip install --upgrade pyinstaller")
        print("  pip install -r requirements.txt")
        print("  python build.py --onedir   # modo alternativo, mais rápido\n")

    # ------------------------------------------------------------------ #
    #  Ponto de entrada                                                    #
    # ------------------------------------------------------------------ #

    def build(
        self,
        modo: str = "onefile",
        windowed: bool = False,
        limpar: bool = True,
        confirmar: bool = True,
    ) -> int:
        """
        Método principal.

        Args:
            modo: ``'onefile'`` ou ``'onedir'``.
            windowed: Ocultar janela de console (quebra o modo CLI).
            limpar: Remover builds anteriores antes de compilar.
            confirmar: Solicitar confirmação interativa antes de iniciar.

        Returns:
            Código de saída (0 = sucesso, 1 = falha/cancelado).
        """
        if not self.verificar_pyinstaller():
            return 1

        if limpar:
            self.limpar_builds_anteriores()

        self.exibir_info(modo, windowed)

        if confirmar:
            resp = input("Continuar? (Y/N): ").strip().lower()
            if resp != "y":
                print("\n✗ Build cancelado.\n")
                return 1

        return self.executar_build(modo, windowed)


# ---------------------------------------------------------------------- #
#  CLI                                                                     #
# ---------------------------------------------------------------------- #

def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Build SCalc com PyInstaller",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python build.py                   # build padrão (onefile, com confirmação)
  python build.py --onedir          # empacota como pasta (inicia mais rápido)
  python build.py --windowed        # oculta console (somente GUI, quebra CLI)
  python build.py -y                # sem confirmação (CI/CD)
  python build.py --no-clean -y     # sem limpar + sem confirmação
""",
    )

    parser.add_argument(
        "--onedir",
        action="store_true",
        help="Empacotar como diretório em vez de arquivo único",
    )
    parser.add_argument(
        "--windowed",
        action="store_true",
        help="Ocultar janela de console no Windows/macOS (ATENÇÃO: desabilita CLI)",
    )
    parser.add_argument(
        "-y", "--yes",
        action="store_true",
        help="Pular confirmação interativa (útil em pipelines CI/CD)",
    )
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Não remover builds anteriores",
    )

    args = parser.parse_args()

    builder = PyInstallerBuilder()
    return builder.build(
        modo="onedir" if args.onedir else "onefile",
        windowed=args.windowed,
        limpar=not args.no_clean,
        confirmar=not args.yes,
    )


if __name__ == "__main__":
    sys.exit(main())
