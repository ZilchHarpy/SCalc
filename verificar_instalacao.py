#!/usr/bin/env python3
"""
SCalc Setup & Verification Script
===================================
Script unificado para verificação e instalação de dependências.
Funciona em Windows, Linux (Ubuntu/Debian, Fedora/RHEL, Arch) e macOS.

Uso:
    python verificar_instalacao.py           # Apenas verifica
    python verificar_instalacao.py --setup   # Verifica e instala
    python verificar_instalacao.py --help    # Mostra ajuda
"""

import sys
import os
import platform
import subprocess
from pathlib import Path


class ScalpSetup:
    """Gerenciador de setup e verificação para SCalc"""
    
    # Dependências Python necessárias
    MODULOS_NECESSARIOS = [
        ('PySide6', 'PySide6'),
        ('matplotlib', 'Matplotlib'),
        ('numpy', 'NumPy'),
        ('pandas', 'Pandas'),
        ('scipy', 'SciPy'),
        ('openpyxl', 'OpenPyXL'),
    ]
    
    def __init__(self):
        self.sistema = platform.system()
        self.distribuicao = self._detectar_distribuicao()
        self.python_exe = sys.executable
        
    def _detectar_distribuicao(self):
        """Detecta a distribuição Linux"""
        if self.sistema == "Linux":
            try:
                with open("/etc/os-release", "r") as f:
                    content = f.read().lower()
                    if "ubuntu" in content or "debian" in content:
                        return "debian"
                    elif "fedora" in content or "rhel" in content:
                        return "fedora"
                    elif "arch" in content:
                        return "arch"
            except:
                pass
        return None
    
    def _banner(self, titulo):
        """Exibe um banner formatado"""
        print()
        print("=" * 60)
        print(f"  {titulo}")
        print("=" * 60)
        print()
    
    def verificar_modulo(self, nome_modulo, nome_exibir=None):
        """Verifica se um módulo Python está instalado"""
        if nome_exibir is None:
            nome_exibir = nome_modulo
        
        try:
            __import__(nome_modulo)
            print(f"  ✓ {nome_exibir:20} instalado")
            return True
        except ImportError:
            print(f"  ✗ {nome_exibir:20} NÃO instalado")
            return False
    
    def verificar_dependencias_python(self):
        """Verifica todas as dependências Python"""
        self._banner("VERIFICAÇÃO DE DEPENDÊNCIAS PYTHON")
        
        resultados = []
        for modulo, exibir in self.MODULOS_NECESSARIOS:
            resultado = self.verificar_modulo(modulo, exibir)
            resultados.append(resultado)
        
        return all(resultados), resultados
    
    def executar_comando(self, cmd, shell=False, descricao=None):
        """Executa um comando do sistema"""
        if descricao:
            print(f"\n  {descricao}...")
        
        try:
            subprocess.run(cmd, shell=shell, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            if descricao:
                print(f"  ⚠ Aviso ao {descricao}")
            return False
        except FileNotFoundError:
            if descricao:
                print(f"  ✗ Comando não encontrado")
            return False
    
    def instalar_dependencias_sistema_linux(self):
        """Instala dependências do sistema no Linux"""
        self._banner("INSTALAÇÃO DE DEPENDÊNCIAS DO SISTEMA (LINUX)")
        
        if not self.distribuicao:
            print("  ⚠ Distribuição não reconhecida automaticamente.")
            print("\n  Instale manualmente uma das opções abaixo:\n")
            print("  Ubuntu/Debian:")
            print("    sudo apt-get update")
            print("    sudo apt-get install -y libxcb-cursor0 libxcb-xinerama0 libxcb-xkb1 libxkbcommon-x11-0\n")
            print("  Fedora/RHEL:")
            print("    sudo dnf install -y libxcb xcb-util-cursor libxkbcommon-x11\n")
            print("  Arch Linux:")
            print("    sudo pacman -Syu --noconfirm libxcb xcb-util-cursor libxkbcommon-x11\n")
            return False
        
        if self.distribuicao == "debian":
            print("  Distribuição detectada: Ubuntu/Debian")
            self.executar_comando("sudo apt-get update", shell=True, descricao="Atualizando repositórios")
            self.executar_comando(
                "sudo apt-get install -y libxcb-cursor0 libxcb-xinerama0 libxcb-xkb1 libxkbcommon-x11-0",
                shell=True,
                descricao="Instalando dependências do sistema"
            )
        
        elif self.distribuicao == "fedora":
            print("  Distribuição detectada: Fedora/RHEL")
            self.executar_comando(
                "sudo dnf install -y libxcb xcb-util-cursor libxkbcommon-x11",
                shell=True,
                descricao="Instalando dependências do sistema"
            )
        
        elif self.distribuicao == "arch":
            print("  Distribuição detectada: Arch Linux")
            self.executar_comando(
                "sudo pacman -Syu --noconfirm libxcb xcb-util-cursor libxkbcommon-x11",
                shell=True,
                descricao="Instalando dependências do sistema"
            )
        
        return True
    
    def instalar_dependencias_sistema_macos(self):
        """Instala dependências do sistema no macOS"""
        self._banner("INSTALAÇÃO DE DEPENDÊNCIAS DO SISTEMA (MACOS)")
        
        # Verificar Homebrew
        resultado = subprocess.run("which brew", shell=True, capture_output=True)
        if resultado.returncode != 0:
            print("  ✗ Homebrew não encontrado.")
            print("\n  Instale em: https://brew.sh\n")
            return False
        
        print("  Homebrew detectado")
        self.executar_comando("brew install qt@6", shell=True, descricao="Instalando Qt6")
        return True
    
    def instalar_dependencias_sistema(self):
        """Instala dependências do sistema conforme o SO"""
        if self.sistema == "Linux":
            return self.instalar_dependencias_sistema_linux()
        elif self.sistema == "Darwin":
            return self.instalar_dependencias_sistema_macos()
        elif self.sistema == "Windows":
            print("\n  Nenhuma dependência adicional do sistema é necessária no Windows.\n")
            return True
        else:
            print(f"\n  ✗ Sistema operacional não suportado: {self.sistema}\n")
            return False
    
    def instalar_dependencias_python(self):
        """Instala dependências Python"""
        self._banner("INSTALAÇÃO DE DEPENDÊNCIAS PYTHON")
        
        requirements_path = Path(__file__).parent / "requirements.txt"
        
        if requirements_path.exists():
            print(f"  Usando {requirements_path.name}...")
            cmd = [self.python_exe, "-m", "pip", "install", "-r", str(requirements_path)]
        else:
            print(f"  Arquivo requirements.txt não encontrado!")
            print("  Instalando dependências manualmente...\n")
            cmd = [
                self.python_exe, "-m", "pip", "install",
                "PySide6", "matplotlib", "numpy", "pandas", "scipy", "openpyxl"
            ]
        
        try:
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError:
            print("  ✗ Erro ao instalar dependências Python")
            return False
    
    def exibir_ajuda(self):
        """Exibe mensagem de ajuda"""
        print()
        print("=" * 60)
        print("  SCalc Setup & Verification Script")
        print("=" * 60)
        print()
        print("Uso:")
        print("  python verificar_instalacao.py           # Apenas verifica")
        print("  python verificar_instalacao.py --setup   # Verifica e instala")
        print("  python verificar_instalacao.py --help    # Mostra esta ajuda")
        print()
        print("Instalação manual:")
        print("  pip install -r requirements.txt")
        print()
        print("Executar o programa:")
        print("  python scalc.py              (Interface gráfica)")
        print("  python scalc.py --cli -f arquivo.xlsx  (Linha de comando)")
        print()
    
    def verificar(self):
        """Apenas verifica as dependências"""
        self._banner("VERIFICAÇÃO DE DEPENDÊNCIAS - SCalc")
        
        print(f"Sistema operacional: {self.sistema}")
        if self.distribuicao:
            print(f"Distribuição detectada: {self.distribuicao.capitalize()}")
        print()
        
        tudo_ok, _ = self.verificar_dependencias_python()
        
        print()
        print("=" * 60)
        
        if tudo_ok:
            print("  ✓ TODAS AS DEPENDÊNCIAS ESTÃO INSTALADAS!")
            print("=" * 60)
            print()
            print("Você pode executar o programa com:")
            print("  python scalc.py")
            print()
            return 0
        else:
            print("  ✗ ALGUMAS DEPENDÊNCIAS FALTAM!")
            print("=" * 60)
            print()
            print("Para instalar, execute:")
            print("  python verificar_instalacao.py --setup")
            print()
            print("Ou instale manualmente:")
            print("  pip install -r requirements.txt")
            print()
            return 1
    
    def setup(self):
        """Realiza setup completo (verificação + instalação)"""
        self._banner("SCALC - SETUP AUTOMÁTICO")
        
        print(f"Sistema operacional: {self.sistema}")
        if self.distribuicao:
            print(f"Distribuição detectada: {self.distribuicao.capitalize()}")
        print()
        
        # Verificar dependências existentes
        tudo_ok, _ = self.verificar_dependencias_python()
        
        if not tudo_ok:
            # Instalar dependências do sistema
            print("\n[1/2] Instalando dependências do sistema...")
            self.instalar_dependencias_sistema()
            
            # Instalar dependências Python
            print("\n[2/2] Instalando dependências Python...")
            if not self.instalar_dependencias_python():
                print("\n✗ Erro durante a instalação!")
                return 1
            
            # Verificar novamente
            print("\nVerificando novamente...")
            tudo_ok, _ = self.verificar_dependencias_python()
        
        # Resultado final
        self._banner("SETUP CONCLUÍDO")
        
        if tudo_ok:
            print("  ✓ TODAS AS DEPENDÊNCIAS FORAM INSTALADAS COM SUCESSO!")
            print()
            print("Para iniciar o programa, execute:")
            print("  python scalc.py")
            print()
            return 0
        else:
            print("  ⚠ Setup concluído, mas algumas dependências podem não estar instaladas.")
            print("    Tente instalar manualmente ou verifique a conexão com a internet.")
            print()
            return 1


def main():
    """Função principal"""
    setup = ScalpSetup()
    
    # Processar argumentos
    if len(sys.argv) > 1:
        argumento = sys.argv[1].lower()
        
        if argumento in ["-h", "--help"]:
            setup.exibir_ajuda()
            return 0
        elif argumento in ["-s", "--setup"]:
            return setup.setup()
        else:
            print(f"Argumento desconhecido: {argumento}\n")
            setup.exibir_ajuda()
            return 1
    else:
        # Por padrão, apenas verifica
        return setup.verificar()


if __name__ == "__main__":
    sys.exit(main())
