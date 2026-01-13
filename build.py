'''
ainda em aperfeiçoamento para criar um executável de forma eficiente e leve...
'''

#!/usr/bin/env python3
"""
Script de build usando Nuitka (compila para C++)
Resultado: executável MUITO mais rápido que PyInstaller
"""

import subprocess
import sys
import platform

def build_nuitka():
    """Build com Nuitka"""
    
    comando = [
        sys.executable, '-m', 'nuitka',
        '--standalone',              # Executável independente
        '--onefile',                 # Arquivo único
        # '--enable-plugin=pyside6',
        '--include-package=PySide6',   # Plugin PySide6
        # '--disable-console',         # Sem console
        '--output-filename=SCalc',   # Nome do executável
        '--include-data-dir=src=src', # Incluir diretório src
        '--include-package=matplotlib',
        '--include-package=numpy',
        '--include-package=pandas',
        '--include-package=scipy',
        '--include-package=openpyxl',
        'scalc.py'
    ]
    
    # Ajustes específicos do Windows
    if platform.system() == 'Windows':
        comando.extend([
            '--windows-icon-from-ico=icon.ico',  # Se tiver ícone
        ])
    
    print("="*60)
    print("BUILD COM NUITKA")
    print("="*60)
    print("\nComando:", ' '.join(comando))
    print("\n⚠️  AVISO: Nuitka demora mais, mas gera executável mais rápido!")
    print("⏱️  Tempo estimado: 5-15 minutos\n")
    
    resultado = subprocess.run(comando)
    
    if resultado.returncode == 0:
        print("\n✓ Build concluído com sucesso!")
        print(f"📦 Executável em: SCalc{'.exe' if platform.system() == 'Windows' else ''}")
    else:
        print("\n❌ Build falhou!")
    
    return resultado.returncode

if __name__ == "__main__":
    # Verificar se Nuitka está instalado
    try:
        import nuitka
        print("✓ Nuitka instalado")
    except ImportError:
        print("❌ Nuitka não instalado!")
        print("\nInstale com:")
        print("  pip install nuitka")
        sys.exit(1)
    
    sys.exit(build_nuitka())
