"""
Script de setup automático para SCalc (Windows)
Este script instala todas as dependências necessárias
"""

import subprocess
import sys
import platform
import os

def run_command(cmd, shell=False):
    """Executa um comando e retorna o código de saída"""
    try:
        result = subprocess.run(cmd, shell=shell, check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        return e.returncode
    except Exception as e:
        print(f"Erro ao executar comando: {e}")
        return 1

def main():
    print("=" * 50)
    print("  SCalc - Setup Automático")
    print("=" * 50)
    print()
    
    # Detectar sistema operacional
    system = platform.system()
    print(f"Sistema detectado: {system}")
    print()
    
    if system == "Linux":
        print("=" * 50)
        print("  Instalando dependências do sistema (Linux)")
        print("=" * 50)
        print()
        
        # Tentar detectar distribuição
        try:
            with open("/etc/os-release", "r") as f:
                os_info = f.read()
                if "debian" in os_info.lower() or "ubuntu" in os_info.lower():
                    print("Distribuição detectada: Ubuntu/Debian")
                    run_command("sudo apt-get update", shell=True)
                    run_command(
                        "sudo apt-get install -y libxcb-cursor0 libxcb-xinerama0 libxcb-xkb1 libxkbcommon-x11-0",
                        shell=True
                    )
                elif "fedora" in os_info.lower() or "rhel" in os_info.lower():
                    print("Distribuição detectada: Fedora/RHEL")
                    run_command("sudo dnf install -y libxcb xcb-util-cursor libxkbcommon-x11", shell=True)
                elif "arch" in os_info.lower():
                    print("Distribuição detectada: Arch Linux")
                    run_command("sudo pacman -Syu --noconfirm libxcb xcb-util-cursor libxkbcommon-x11", shell=True)
                else:
                    print("Distribuição não reconhecida automaticamente.")
                    print("Tente instalar manualmente:")
                    print("Ubuntu/Debian: sudo apt-get install libxcb-cursor0 libxcb-xinerama0 libxcb-xkb1 libxkbcommon-x11-0")
                    print("Fedora/RHEL: sudo dnf install libxcb xcb-util-cursor libxkbcommon-x11")
                    print("Arch Linux: sudo pacman -S libxcb xcb-util-cursor libxkbcommon-x11")
        except:
            print("Não foi possível detectar a distribuição Linux.")
            print("Tente instalar manualmente as dependências do sistema.")
    
    elif system == "Darwin":
        print("=" * 50)
        print("  Instalando dependências do sistema (macOS)")
        print("=" * 50)
        print()
        
        if os.system("which brew > /dev/null 2>&1") != 0:
            print("Homebrew não encontrado.")
            print("Instale em: https://brew.sh")
            sys.exit(1)
        
        run_command("brew install qt@6", shell=True)
    
    elif system == "Windows":
        print("Sistema detectado: Windows")
        print("Nenhuma dependência adicional do sistema é necessária.")
        print()
    
    # Instalar dependências Python
    print("=" * 50)
    print("  Instalando dependências Python")
    print("=" * 50)
    print()
    
    if os.path.exists("requirements.txt"):
        print("Usando requirements.txt...")
        run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    else:
        print("Arquivo requirements.txt não encontrado!")
        print("Instalando dependências manualmente...")
        run_command([
            sys.executable, "-m", "pip", "install",
            "PySide6", "matplotlib", "numpy", "pandas", "scipy", "openpyxl"
        ])
    
    print()
    print("=" * 50)
    print("  Setup concluído com sucesso!")
    print("=" * 50)
    print()
    print("Para iniciar o programa, execute:")
    print("  python scalc.py")
    print()

if __name__ == "__main__":
    main()
