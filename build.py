#!/usr/bin/env python3
"""
Script de build usando Nuitka (compila para C++)
Características:
- Compila Python para C++ nativo
- Muito mais rápido que PyInstaller
- Suporta Windows, Linux e macOS
- Opções de build: onefile ou standalone
"""

import subprocess
import sys
import platform
import os
import shutil
from pathlib import Path
from datetime import datetime

class NuitkaBuilder:
    """Gerenciador de build com Nuitka"""

    def __init__(self):
        self.sistema = platform.system()
        self.arquitetura = platform.machine()
        self.python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        self.project_root = Path(__file__).parent
        self.dist_dir = self.project_root / 'dist'

    def verificar_nuitka(self):
        """Verifica se Nuitka está instalado"""
        try:
            import nuitka
            print("✓ Nuitka instalado")
            return True
        except ImportError:
            print("❌ Nuitka não instalado!")
            print("\nInstale com:")
            print("  pip install nuitka")
            return False
        
    def verificar_compilador(self):
        """Verifica se o compilador C++ está disponível"""
        if self.sistema == 'Windows':
            print("ℹ️  Windows: Nuitka baixará MinGW64 automaticamente se necessário")
            return True
        elif self.sistema == 'Linux':
            resultado = subprocess.run('gcc --version', shell=True, capture_output=True)
            if resultado.returncode == 0:
                print("✓ GCC encontrado")
                return True
            else:
                print("⚠️  GCC não encontrado!")
                print("   Instale com: sudo apt install build-essential")
                return False
        elif self.sistema == 'Darwin':  # macOS
            resultado = subprocess.run('xcode-select -p', shell=True, capture_output=True)
            if resultado.returncode == 0:
                print("✓ Xcode Command Line Tools encontrado")
                return True
            else:
                print("⚠️  Xcode Command Line Tools não encontrado!")
                print("   Instale com: xcode-select --install")
                return False
        return True # Para outros sistemas, confiar que o compilador está presente
    
    def limpar_builds_anteriores(self):
        """Remove builds anteriores"""
        dirs_limpar = ['build', 'dist', '__pycache__']
        
        for dir_name in dirs_limpar:
            dir_path = self.project_root / dir_name
            if dir_path.exists():
                print(f"🗑️  Removendo {dir_name}/")
                shutil.rmtree(dir_path, ignore_errors=True)
    
    def get_comando_nuitka(self, modo: str = 'onefile') -> list:
        """
        Gera o comando Nuitka com todas as flags
        
        Args:
            modo: 'onefile' ou 'standalone'
        """
        comando = [
            sys.executable, '-m', 'nuitka',
            
            # ===== MODO DE BUILD =====
            '--standalone',  # Sempre standalone
        ]
        
        # Adicionar --onefile se solicitado
        if modo == 'onefile':
            comando.append('--onefile')
        
        # ===== PLUGINS E INCLUDES =====
        comando.extend([
            # Plugin PySide6 (crítico!)
            '--enable-plugin=pyside6',
            
            # Incluir pacotes completos
            '--include-package=matplotlib',
            '--include-package=numpy',
            '--include-package=pandas',
            '--include-package=scipy',
            '--include-package=openpyxl',
            '--include-package=src',  # TODO nosso código
            
            # Incluir módulos específicos que podem ser importados dinamicamente
            '--include-module=src.visualization.gui',
            '--include-module=src.core',
            '--include-module=src.utils',
        ])
        
        # ===== OTIMIZAÇÕES =====
        comando.extend([
            '--lto=yes',  # Link Time Optimization
            '--assume-yes-for-downloads',  # Download automático de dependências
        ])
        
        # ===== OUTPUT =====
        comando.extend([
            '--output-dir=dist',
            '--output-filename=SCalc',
        ])
        
        # ===== CONFIGURAÇÕES ESPECÍFICAS DO SO =====
        if self.sistema == 'Windows':
            comando.extend([
                '--windows-console-mode=disable',  # Remove console preto
                '--windows-company-name=Caio Aquilino Merino',
                '--windows-product-name=SCalc',
                '--windows-product-version=1.0.0',
                '--windows-file-description=Sistema de Análise de Regressão Linear',
            ])
            
            # Ícone (se existir)
            icone_path = self.project_root / 'assets' / 'icon.ico'
            if icone_path.exists():
                comando.append(f'--windows-icon-from-ico={icone_path}')
        
        elif self.sistema == 'Linux':
            comando.extend([
                '--linux-icon=assets/icon.png',  # Se tiver
            ])
        
        elif self.sistema == 'Darwin':  # macOS
            comando.extend([
                '--macos-create-app-bundle',
                '--macos-app-name=SCalc',
            ])
        
        # ===== ARQUIVO PRINCIPAL =====
        comando.append('scalc.py')
        
        return comando
    
    def exibir_info_build(self, modo: str):
        """Exibe informações sobre o build"""
        print("\n" + "="*70)
        print(f"  BUILD COM NUITKA - SCalc v1.0")
        print("="*70)
        print(f"\n📊 Informações do Sistema:")
        print(f"   Sistema Operacional: {self.sistema}")
        print(f"   Arquitetura: {self.arquitetura}")
        print(f"   Python: {self.python_version}")
        print(f"\n📦 Configuração de Build:")
        print(f"   Modo: {modo.upper()}")
        print(f"   Diretório de saída: {self.dist_dir}")

        # Estimativas
        if modo == 'onefile':
            print(f"\n📏 Estimativas:")
            print(f"   Tamanho final: ~200-250 MB")
            print(f"   Tempo de build: 10-30 minutos")
            print(f"   Tempo de inicialização: ~2-5 segundos")
        
        else:
            print(f"\n📏 Estimativas:")
            print(f"   Tamanho final: ~300-400 MB (múltiplos arquivos)")
            print(f"   Tempo de build: 10-30 minutos")
            print(f"   Tempo de inicialização: <1 segundo")
        
        print(f"\n⚠️  Avisos:")
        print(f"   • Primeira compilação é lenta!")
        print(f"   • Requer ~2GB de RAM durante compilação")
        print(f"   • Não feche o terminal durante o processo")

    def confirmar_build(self) -> bool:
        """Solicita confirmação do usuário"""
        print("\n" + "-"*70)
        resposta = input("Deseja continuar com o build? (Y/N): ").strip().lower()
        return resposta == 'y'
    
    def executar_build(self, modo: str = 'onefile') -> int:
        """
        Executa o build
        
        Args:
            modo: 'onefile' ou 'standalone'
            
        Returns:
            int: 0 se sucesso, 1 se falha
        """
        inicio = datetime.now()
        
        comando = self.get_comando_nuitka(modo)
        
        print("\n🚀 Iniciando compilação...")
        print(f"\n💻 Comando:\n   {' '.join(comando)}\n")
        print("-"*70)
        print("Aguarde... (isso pode demorar 10-30 minutos)")
        print("-"*70 + "\n")

        # Executar Nuitka
        resultado = subprocess.run(comando)
        
        fim = datetime.now()
        duracao = fim - inicio

        if resultado.returncode == 0:
            self.exibir_sucesso(modo, duracao)
            return 0
        else:
            self.exibir_falha()
            return 1
        
    def exibir_sucesso(self, modo: str, duracao):
        """Exibe mensagem de sucesso"""
        print("\n" + "="*70)
        print("  ✅ BUILD CONCLUÍDO COM SUCESSO!")
        print("="*70)
        
        # Localizar executável
        if self.sistema == 'Windows':
            exe_nome = 'SCalc.exe'
        else:
            exe_nome = 'SCalc'
        
        if modo == 'onefile':
            exe_path = self.dist_dir / exe_nome
        else:
            exe_path = self.dist_dir / 'SCalc.dist' / exe_nome
        
        print(f"\n📦 Executável criado:")
        print(f"   Localização: {exe_path}")
        
        # Tamanho do arquivo
        if exe_path.exists():
            tamanho_bytes = exe_path.stat().st_size
            tamanho_mb = tamanho_bytes / (1024 * 1024)
            print(f"   Tamanho: {tamanho_mb:.1f} MB")
        
        print(f"\n⏱️  Tempo de compilação: {duracao}")
        
        print("\n💡 Próximos passos:")
        print("   1. Teste o executável:")
        if self.sistema == 'Windows':
            print(f"      {exe_path}")
        else:
            print(f"      ./{exe_path}")
        print("   2. Teste em uma máquina limpa (sem Python)")
        print("   3. Crie um instalador com Inno Setup (Windows)")
        print("   4. Publique no GitHub Releases")
        print("")

    def exibir_falha(self):
        """Exibe mensagem de falha"""
        print("\n" + "="*70)
        print("  ❌ BUILD FALHOU!")
        print("="*70)
        print("\n🔧 Troubleshooting:")
        print("\n1. Verificar compilador C++:")
        if self.sistema == 'Windows':
            print("   Nuitka deve baixar MinGW64 automaticamente")
            print("   Se falhar, baixe manualmente de: https://nuitka.net/doc/user-manual.html")
        elif self.sistema == 'Linux':
            print("   sudo apt install build-essential")
        elif self.sistema == 'Darwin':
            print("   xcode-select --install")
        
        print("\n2. Verificar memória RAM:")
        print("   Build requer ~2GB livres")
        
        print("\n3. Tentar modo standalone (mais rápido):")
        print("   python build.py --standalone")
        
        print("\n4. Verificar logs acima para erros específicos")
        print("")

    def build(self, modo: str = 'onefile', limpar: bool = True, confirmar: bool = True):
        """
        Método principal de build
        
        Args:
            modo: 'onefile' ou 'standalone'
            limpar: Se deve limpar builds anteriores
            confirmar: Se deve pedir confirmação do usuário
        """
        print("="*70)
        print("  NUITKA BUILD SYSTEM - SCalc")
        print("="*70)
        
        # Verificações
        if not self.verificar_nuitka():
            return 1
        
        if not self.verificar_compilador():
            print("\n⚠️  Compilador não encontrado, mas continuando...")
            print("   (Nuitka tentará resolver automaticamente)\n")
        
        # Limpar builds anteriores
        if limpar:
            self.limpar_builds_anteriores()
        
        # Exibir informações
        self.exibir_info_build(modo)
        
        # Confirmar
        if confirmar and not self.confirmar_build():
            print("\n❌ Build cancelado pelo usuário\n")
            return 1
        
        # Executar build
        return self.executar_build(modo)
    

def main():
    """Função principal"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Build SCalc com Nuitka',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Exemplos:

  # Build padrão (onefile):
  python build.py
  
  # Build standalone (mais rápido de iniciar):
  python build.py --standalone
  
  # Sem confirmação (para CI/CD):
  python build.py --yes
  
  # Sem limpar builds anteriores:
  python build.py --no-clean
        '''
    )

    parser.add_argument(
        '--standalone',
        action='store_true',
        help='Build em modo standalone (múltiplos arquivos, inicia mais rápido)'
    )

    parser.add_argument(
        '--yes', '-y',
        action='store_true',
        help='Não pedir confirmação (útil para scripts automatizados)'
    )

    parser.add_argument(
        '--no-clean',
        action='store_true',
        help='Não limpar builds anteriores'
    )

    args = parser.parse_args()

    # Determinar modo
    modo = 'standalone' if args.standalone else 'onefile'

    # Criar builder e executar
    builder = NuitkaBuilder()
    return builder.build(
        modo=modo,
        limpar=not args.no_clean,
        confirmar=not args.yes
    )

if __name__ == '__main__':
    sys.exit(main())