#!/usr/bin/env python3
"""
SCalc Setup & Verification Script
===================================
Script unificado para verificação e instalação de dependências.
Funciona em Windows, Linux (Ubuntu/Debian, Fedora/RHEL, Arch) e macOS.

Uso:
    python setup.py             # Verifica e instala (com confirmação do usuário)
"""

import sys
import os
import platform
import subprocess
from pathlib import Path


class ScalcSetup:
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
        self.distribuicao = self._detectar_distro()
        self.python_exe = sys.executable
        
    def _detectar_distro(self):
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
        
        instaladas = []
        nao_instaladas = []
        
        for modulo, exibir in self.MODULOS_NECESSARIOS:
            if self.verificar_modulo(modulo, exibir):
                instaladas.append(exibir)
            else:
                nao_instaladas.append(exibir)
        
        return len(nao_instaladas) == 0, nao_instaladas
    
    def instalar_dependencias_python(self):
        """Instala dependências Python"""
        self._banner("INSTALAÇÃO DE DEPENDÊNCIAS PYTHON")
        
        requirements_path = Path(__file__).parent / "requirements.txt"
        
        if requirements_path.exists():
            print(f"  Usando {requirements_path.name}...")
            cmd = [self.python_exe, "-m", "pip", "install", "-r", str(requirements_path)]
        else:
            print(f"  Arquivo requirements.txt não encontrado!")
            print("   Deseja instalar as seguintes dependências? (Y/N)\n")
            print("   <PySide6, matplotlib, numpy, pandas, scipy, openpyxl>\n")
            resposta = input("   >>: ").strip().lower()
            if resposta == 'n':
                print("  ✗ Instalação das dependências python cancelada pelo usuário.\n")
                return False
            elif resposta == 'y':
                print("  Iniciando instalação das dependências...\n")
                cmd = [
                    self.python_exe, "-m", "pip", "install",
                    "PySide6", "matplotlib", "numpy", "pandas", "scipy", "openpyxl"
                ]
            else:
                print("  Resposta inválida. Cancelando a instalação das dependências python...\n") 
                return False
        
        try:
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError:
            print("  ✗ Erro ao instalar dependências Python")
            return False
    
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
    
    def verificar_dependencias(self):
        """Verifica as dependências"""
        self._banner("VERIFICAÇÃO DE DEPENDÊNCIAS - SCalc")
        
        print(f"Sistema operacional: {self.sistema}")
        if self.distribuicao:
            print(f"Distribuição detectada: {self.distribuicao.capitalize()}")
        print()
        
        tudo_ok, nao_instaladas = self.verificar_dependencias_python()
        
        return tudo_ok, nao_instaladas
    
    def setup(self):
        """Verifica e instala dependências conforme necessário"""
        # Verificar dependências
        tudo_ok, nao_instaladas = self.verificar_dependencias()
        
        if tudo_ok:
            self._banner("SETUP CONCLUÍDO")
            print("  ✓ TODAS AS DEPENDÊNCIAS JÁ ESTÃO INSTALADAS!")
            print()
            print("Para iniciar o programa, execute:")
            print("  python scalc.py")
            print()
            return 0
        
        # Se faltam dependências, pedir confirmação
        print("\nDeseja instalar as dependências ausentes? (Y/N): ", end="")
        resposta = input().strip().lower()
        if resposta == 'n':
            print("\n✗ Instalação cancelada pelo usuário.\n")
            return 1
        elif resposta == 'y':
            print("\nIniciando instalação das dependências...\n")
        else:
            print("\nResposta inválida. Cancelando a instalação...\n")
            print("  ✗ Instalação cancelada.\n")
            return 1
        
        # Instalar dependências do sistema automaticamente
        print("\n[1/2] Instalando dependências do sistema...")
        if not self.instalar_dependencias_sistema():
            print("  ⚠ Aviso: Algumas dependências do sistema podem não ter sido instaladas.")
        
        # Instalar dependências Python
        print("\n[2/2] Instalando dependências Python...")
        if not self.instalar_dependencias_python():
            print("\n✗  A instalação foi impedida ou falhou!")
            return 1
        
        # Verificar novamente
        print("\nVerificando novamente...")
        tudo_ok, _ = self.verificar_dependencias()
        
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
            print("    Tente novamente ou verifique a conexão com a internet.")
            print()
            return 1


def main():
    """
    Função principal.
    Verifica e instala dependências necessárias do sistema e do Python para o SCalc.
    """
    setup = ScalcSetup()
    setup._banner("SCALC - SETUP")
    return setup.setup()


if __name__ == "__main__":
    sys.exit(main())

