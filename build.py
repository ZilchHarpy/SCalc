'''
ainda em aperfeicoamento para criar um executavel de forma eficiente e leve...
'''

#!/usr/bin/env python3
"""
Script de build usando Nuitka (compila para C++)
Resultado: executavel MUITO mais rapido que PyInstaller
"""

import subprocess
import sys
import platform

def build_nuitka():
    """Build com Nuitka"""
    
    comando = [
        sys.executable, '-m', 'nuitka',
        '--standalone',              # Executavel independente
        '--onefile',                 # Arquivo unico
        # '--enable-plugin=pyside6',
        '--include-package=PySide6',   # Plugin PySide6
        # '--disable-console',         # Sem console
        '--output-filename=SCalc',   # Nome do executavel
        '--include-data-dir=src=src', # Incluir diretorio src
        '--include-package=matplotlib',
        '--include-package=numpy',
        '--include-package=pandas',
        '--include-package=scipy',
        '--include-package=openpyxl',
        'scalc.py'
    ]
    
    # Ajustes especificos do Windows
    if platform.system() == 'Windows':
        comando.extend([
            '--windows-icon-from-ico=icon.ico',  # Se tiver icone
        ])
    
    print("="*60)
    print("BUILD COM NUITKA")
    print("="*60)
    print("\nComando:", ' '.join(comando))
    print("\n⚠️  AVISO: Nuitka demora mais, mas gera executavel mais rapido!")
    print("⏱️  Tempo estimado: 5-15 minutos\n")
    
    resultado = subprocess.run(comando)
    
    if resultado.returncode == 0:
        print("\n✓ Build concluido com sucesso!")
        print(f"📦 Executavel em: SCalc{'.exe' if platform.system() == 'Windows' else ''}")
    else:
        print("\n❌ Build falhou!")
    
    return resultado.returncode

if __name__ == "__main__":
    # Verificar se Nuitka esta instalado
    try:
        import nuitka
        print("✓ Nuitka instalado")
    except ImportError:
        print("❌ Nuitka nao instalado!")
        print("\nInstale com:")
        print("  pip install nuitka")
        sys.exit(1)
    
    sys.exit(build_nuitka())
