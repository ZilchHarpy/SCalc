#!/usr/bin/env python3
"""
Script de teste para verificar se todas as dependências estão instaladas corretamente
"""

import sys

def verificar_modulo(nome_modulo, nome_exibir=None):
    """Verifica se um módulo está instalado"""
    if nome_exibir is None:
        nome_exibir = nome_modulo
    
    try:
        __import__(nome_modulo)
        print(f"✓ {nome_exibir:20} instalado")
        return True
    except ImportError:
        print(f"✗ {nome_exibir:20} NÃO instalado")
        return False

def main():
    print("=" * 60)
    print("VERIFICAÇÃO DE DEPENDÊNCIAS - SCalc")
    print("=" * 60)
    print()
    
    modulos = [
        ('PySide6', 'PySide6'),
        ('matplotlib', 'Matplotlib'),
        ('numpy', 'NumPy'),
        ('pandas', 'Pandas'),
        ('scipy', 'SciPy'),
        ('openpyxl', 'OpenPyXL'),
    ]
    
    resultados = []
    
    for modulo, exibir in modulos:
        resultado = verificar_modulo(modulo, exibir)
        resultados.append(resultado)
    
    print()
    print("=" * 60)
    
    if all(resultados):
        print("✓ TODAS AS DEPENDÊNCIAS INSTALADAS!")
        print()
        print("Você pode executar o programa com:")
        print("  python scalc.py              (Interface gráfica)")
        print("  python scalc.py --cli -f arquivo.xlsx  (Linha de comando)")
        return 0
    else:
        print("✗ ALGUMAS DEPENDÊNCIAS FALTANDO!")
        print()
        print("Instale as dependências faltantes com:")
        print("  pip install PySide6 matplotlib numpy pandas scipy openpyxl")
        print()
        print("Ou use o requirements.txt:")
        print("  pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())
