#!/bin/bash

# Script de setup automático para SCalc
# Este script instala todas as dependências necessárias

echo "================================================"
echo "  SCalc - Setup Automático"
echo "================================================"
echo ""

# Detectar sistema operacional
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Sistema detectado: Linux"
    
    # Detectar distribuição
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$ID
    fi
    
    case $OS in
        ubuntu|debian)
            echo "Instalando dependências do sistema (Ubuntu/Debian)..."
            sudo apt-get update
            sudo apt-get install -y libxcb-cursor0 libxcb-xinerama0 libxcb-xkb1 libxkbcommon-x11-0
            ;;
        fedora|rhel)
            echo "Instalando dependências do sistema (Fedora/RHEL)..."
            sudo dnf install -y libxcb xcb-util-cursor libxkbcommon-x11
            ;;
        arch)
            echo "Instalando dependências do sistema (Arch Linux)..."
            sudo pacman -Syu --noconfirm libxcb xcb-util-cursor libxkbcommon-x11
            ;;
        *)
            echo "Distribuição não reconhecida. Tente instalar manualmente:"
            echo "Ubuntu/Debian: sudo apt-get install libxcb-cursor0 libxcb-xinerama0 libxcb-xkb1 libxkbcommon-x11-0"
            echo "Fedora/RHEL: sudo dnf install libxcb xcb-util-cursor libxkbcommon-x11"
            echo "Arch Linux: sudo pacman -S libxcb xcb-util-cursor libxkbcommon-x11"
            ;;
    esac
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Sistema detectado: macOS"
    echo "Instalando dependências do sistema (macOS)..."
    if ! command -v brew &> /dev/null; then
        echo "Homebrew não encontrado. Instale em https://brew.sh"
        exit 1
    fi
    brew install qt@6
    
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "Sistema detectado: Windows"
    echo "Nenhuma dependência adicional é necessária no Windows"
    
else
    echo "Sistema operacional não reconhecido"
    exit 1
fi

echo ""
echo "================================================"
echo "  Instalando dependências Python"
echo "================================================"
echo ""

# Verificar se pip está disponível
if ! command -v pip &> /dev/null; then
    echo "Erro: pip não encontrado. Instale Python 3.8 ou superior."
    exit 1
fi

# Instalar dependências Python
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo "Arquivo requirements.txt não encontrado!"
    echo "Instalando dependências manualmente..."
    pip install PySide6 matplotlib numpy pandas scipy openpyxl
fi

echo ""
echo "================================================"
echo "  Setup concluído com sucesso!"
echo "================================================"
echo ""
echo "Para iniciar o programa, execute:"
echo "  python scalc.py"
echo ""
