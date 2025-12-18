#!/usr/bin/env python3
"""
Setup Script para SCalc
=======================
Este script é um atalho para executar:
    python verificar_instalacao.py --setup

Para mais informações, veja verificar_instalacao.py
"""

import subprocess
import sys

if __name__ == "__main__":
    # Executar o setup unificado
    resultado = subprocess.run([sys.executable, "verificar_instalacao.py", "--setup"])
    sys.exit(resultado.returncode)
