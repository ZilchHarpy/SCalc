"""
Modulo de Interface Grafica (GUI)

Contem a interface grafica principal do SCalc usando PySide6.
"""

import sys
import numpy as np
import pandas as pd
from matplotlib.backends.backend_qt import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit, QFileDialog,
    QTableWidget, QTableWidgetItem, QGroupBox, QComboBox,
    QTabWidget, QMessageBox, QSplitter
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

# Importar funcoes utilitarias da nova estrutura
from src.core import calcular_estatisticas, RegLin


class MplCanvas(FigureCanvas):
    """Canvas do Matplotlib integrado ao Qt"""
    def __init__(self, parent=None, width=8, height=6, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)


class InterfaceRegressaoLinear(QMainWindow):
    """Interface grafica principal para analise de regressao linear"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SCalc - Sistema de Calculo e Analise de Regressao Linear")
        self.setGeometry(50, 50, 1400, 900)
        
        # Variaveis de dados
        self.dados_excel = None
        self.medias = {}
        self.err_est = {}
        self.err_instr = {}
        self.data_x = None
        self.data_y = None
        self.data_x_err = None
        self.data_y_err = None
        self.slope = None
        self.intercept = None
        self.r_squared = None
        self.caminho_arquivo = None
        
        # Configurar interface
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface do usuario"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Criar splitter para dividir painel de controle e visualizacao
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # ============ PAINEL ESQUERDO - CONTROLES ============
        painel_esquerdo = QWidget()
        layout_esquerdo = QVBoxLayout(painel_esquerdo)
        
        # Titulo
        titulo_label = QLabel("📊 SCalc - Analise de Regressao")
        titulo_font = QFont()
        titulo_font.setPointSize(14)
        titulo_font.setBold(True)
        titulo_label.setFont(titulo_font)
        titulo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_esquerdo.addWidget(titulo_label)
        
        # Grupo: Carregar Dados
        grupo_arquivo = QGroupBox("1. Carregar Arquivo")
        layout_arquivo = QVBoxLayout()
        
        self.label_arquivo = QLabel("Nenhum arquivo carregado")
        self.label_arquivo.setWordWrap(True)
        layout_arquivo.addWidget(self.label_arquivo)
        
        btn_carregar = QPushButton("📁 Selecionar Arquivo Excel")
        btn_carregar.clicked.connect(self.carregar_arquivo)
        layout_arquivo.addWidget(btn_carregar)
        
        grupo_arquivo.setLayout(layout_arquivo)
        layout_esquerdo.addWidget(grupo_arquivo)
        
        # Grupo: Configuracoes dos Eixos
        grupo_eixos = QGroupBox("2. Configurar Eixos")
        layout_eixos = QVBoxLayout()
        
        layout_eixos.addWidget(QLabel("Eixo X (label):"))
        self.entrada_x = QLineEdit("log(t) [s]")
        layout_eixos.addWidget(self.entrada_x)
        
        layout_eixos.addWidget(QLabel("Eixo Y (label):"))
        self.entrada_y = QLineEdit("log(d) [mm]")
        layout_eixos.addWidget(self.entrada_y)
        
        layout_eixos.addWidget(QLabel("Titulo do Grafico:"))
        self.entrada_titulo = QLineEdit("Grafico de Dispersao com Regressao Linear")
        layout_eixos.addWidget(self.entrada_titulo)
        
        grupo_eixos.setLayout(layout_eixos)
        layout_esquerdo.addWidget(grupo_eixos)
        
        # Grupo: Selecao de Variaveis
        grupo_variaveis = QGroupBox("3. Selecionar Variaveis")
        layout_variaveis = QVBoxLayout()
        
        layout_variaveis.addWidget(QLabel("Variavel X (independente):"))
        self.combo_var_x = QComboBox()
        layout_variaveis.addWidget(self.combo_var_x)
        
        layout_variaveis.addWidget(QLabel("Variavel Y (dependente):"))
        self.combo_var_y = QComboBox()
        layout_variaveis.addWidget(self.combo_var_y)
        
        grupo_variaveis.setLayout(layout_variaveis)
        layout_esquerdo.addWidget(grupo_variaveis)
        
        # Grupo: Acoes
        grupo_acoes = QGroupBox("4. Acoes")
        layout_acoes = QVBoxLayout()
        
        self.btn_calcular = QPushButton("🔢 Calcular Estatisticas")
        self.btn_calcular.clicked.connect(self.calcular_estatisticas)
        self.btn_calcular.setEnabled(False)
        layout_acoes.addWidget(self.btn_calcular)
        
        self.btn_regressao = QPushButton("📈 Calcular Regressao Linear")
        self.btn_regressao.clicked.connect(self.calcular_regressao)
        self.btn_regressao.setEnabled(False)
        layout_acoes.addWidget(self.btn_regressao)
        
        self.btn_plotar = QPushButton("🎨 Plotar Grafico")
        self.btn_plotar.clicked.connect(self.plotar_grafico)
        self.btn_plotar.setEnabled(False)
        layout_acoes.addWidget(self.btn_plotar)
        
        btn_limpar = QPushButton("🗑️ Limpar Tudo")
        btn_limpar.clicked.connect(self.limpar_tudo)
        layout_acoes.addWidget(btn_limpar)
        
        grupo_acoes.setLayout(layout_acoes)
        layout_esquerdo.addWidget(grupo_acoes)
        
        # Area de Resultados
        grupo_resultados = QGroupBox("📋 Resultados")
        layout_resultados = QVBoxLayout()
        
        self.texto_resultados = QTextEdit()
        self.texto_resultados.setReadOnly(True)
        self.texto_resultados.setMaximumHeight(200)
        layout_resultados.addWidget(self.texto_resultados)
        
        grupo_resultados.setLayout(layout_resultados)
        layout_esquerdo.addWidget(grupo_resultados)
        
        # Espacador
        layout_esquerdo.addStretch()
        
        # ============ PAINEL DIREITO - VISUALIZACAO ============
        painel_direito = QWidget()
        layout_direito = QVBoxLayout(painel_direito)
        
        # Tabs para diferentes visualizacoes
        self.tabs = QTabWidget()
        
        # Tab 1: Grafico
        tab_grafico = QWidget()
        layout_tab_grafico = QVBoxLayout(tab_grafico)
        
        # Canvas do Matplotlib
        self.canvas = MplCanvas(self, width=10, height=8, dpi=100)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        layout_tab_grafico.addWidget(self.toolbar)
        layout_tab_grafico.addWidget(self.canvas)
        
        self.tabs.addTab(tab_grafico, "📊 Grafico")
        
        # Tab 2: Dados
        tab_dados = QWidget()
        layout_tab_dados = QVBoxLayout(tab_dados)
        
        self.tabela_dados = QTableWidget()
        layout_tab_dados.addWidget(self.tabela_dados)
        
        self.tabs.addTab(tab_dados, "📄 Dados")
        
        # Tab 3: Estatisticas Detalhadas
        tab_estatisticas = QWidget()
        layout_tab_estatisticas = QVBoxLayout(tab_estatisticas)
        
        self.texto_estatisticas = QTextEdit()
        self.texto_estatisticas.setReadOnly(True)
        layout_tab_estatisticas.addWidget(self.texto_estatisticas)
        
        self.tabs.addTab(tab_estatisticas, "📈 Estatisticas")
        
        layout_direito.addWidget(self.tabs)
        
        # Adicionar paineis ao splitter
        splitter.addWidget(painel_esquerdo)
        splitter.addWidget(painel_direito)
        splitter.setStretchFactor(0, 1)  # Painel esquerdo: 1 parte
        splitter.setStretchFactor(1, 2)  # Painel direito: 2 partes
        
        main_layout.addWidget(splitter)
        
        # Plotar grid inicial
        self.plotar_grid_inicial()
    
    def plotar_grid_inicial(self):
        """Plota um grid vazio inicial"""
        self.canvas.axes.clear()
        self.canvas.axes.set_xlabel('x', fontsize=12)
        self.canvas.axes.set_ylabel('y', fontsize=12)
        self.canvas.axes.set_title('Aguardando dados...', fontsize=14)
        self.canvas.axes.grid(True, alpha=0.3, linestyle='--')
        self.canvas.axes.axhline(y=0, color='k', linewidth=0.5)
        self.canvas.axes.axvline(x=0, color='k', linewidth=0.5)
        self.canvas.draw()
    
    def carregar_arquivo(self):
        """Carrega arquivo Excel"""
        caminho, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar Arquivo Excel",
            "",
            "Arquivos Excel (*.xlsx *.xls)"
        )
        
        if not caminho:
            return
        
        try:
            self.caminho_arquivo = caminho
            self.dados_excel = pd.read_excel(caminho)
            
            self.label_arquivo.setText(f"✓ Arquivo carregado:\n{caminho.split('/')[-1]}")
            self.texto_resultados.setText(f"✓ Arquivo carregado com sucesso!\n\nLinhas: {len(self.dados_excel)}\nColunas: {len(self.dados_excel.columns)}")
            
            # Mostrar dados na tabela
            self.mostrar_dados_tabela()
            
            # Habilitar botao de calcular
            self.btn_calcular.setEnabled(True)
            
            # Popular combos de variaveis (apos calcular estatisticas)
            self.texto_resultados.append("\n⚠️ Clique em 'Calcular Estatisticas' para continuar.")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar arquivo:\n{str(e)}")
            self.texto_resultados.setText(f"❌ Erro ao carregar arquivo:\n{str(e)}")
    
    def mostrar_dados_tabela(self):
        """Mostra os dados carregados na tabela"""
        if self.dados_excel is None:
            return
        
        df = self.dados_excel
        
        # Configurar tabela
        self.tabela_dados.setRowCount(len(df))
        self.tabela_dados.setColumnCount(len(df.columns))
        self.tabela_dados.setHorizontalHeaderLabels([str(col) for col in df.columns])
        
        # Preencher dados
        for i in range(len(df)):
            for j in range(len(df.columns)):
                valor = df.iloc[i, j]
                if pd.notna(valor):
                    self.tabela_dados.setItem(i, j, QTableWidgetItem(str(valor)))
        
        self.tabela_dados.resizeColumnsToContents()
    
    def calcular_estatisticas(self):
        """Calcula medias e erros estatisticos"""
        if self.dados_excel is None:
            QMessageBox.warning(self, "Aviso", "Por favor, carregue um arquivo primeiro!")
            return
        
        try:
            # Calcular estatisticas
            resultado_stats = calcular_estatisticas(self.dados_excel)
            
            # Extrair dados do DataFrame
            self.medias = dict(zip(resultado_stats['Dados'], resultado_stats['Media']))
            self.err_est = dict(zip(resultado_stats['Dados'], resultado_stats['S_err']))
            self.err_instr = dict(zip(resultado_stats['Dados'], resultado_stats['T_err']))
            
            # Popular combos com as variaveis disponiveis
            variaveis = list(self.medias.keys())
            self.combo_var_x.clear()
            self.combo_var_y.clear()
            self.combo_var_x.addItems(variaveis)
            self.combo_var_y.addItems(variaveis)
            
            # Selecionar padrao (se houver pelo menos 2 variaveis)
            if len(variaveis) >= 2:
                self.combo_var_x.setCurrentIndex(1)  # Segunda variavel para X
                self.combo_var_y.setCurrentIndex(0)  # Primeira variavel para Y
            
            # Mostrar estatisticas detalhadas
            self.mostrar_estatisticas_detalhadas()
            
            self.texto_resultados.setText(f"✓ Estatisticas calculadas!\n\nVariaveis encontradas: {', '.join(variaveis)}\n\n⚠️ Selecione as variaveis X e Y e clique em 'Calcular Regressao Linear'.")
            
            # Habilitar proximo botao
            self.btn_regressao.setEnabled(True)
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao calcular estatisticas:\n{str(e)}")
            self.texto_resultados.setText(f"❌ Erro ao calcular estatisticas:\n{str(e)}")
    
    def mostrar_estatisticas_detalhadas(self):
        """Mostra estatisticas detalhadas na tab correspondente"""
        if not self.medias:
            return
        
        texto = "=" * 60 + "\n"
        texto += "ESTATISTICAS DETALHADAS\n"
        texto += "=" * 60 + "\n\n"
        
        for var in self.medias.keys():
            texto += f"Variavel: {var}\n"
            texto += "-" * 40 + "\n"
            texto += f"Medias: {self.medias[var]}\n"
            if var in self.err_est:
                texto += f"Erros Estatisticos: {self.err_est[var]}\n"
            if var in self.err_instr:
                texto += f"Erros Instrumentais: {self.err_instr[var]}\n"
            texto += "\n"
        
        self.texto_estatisticas.setText(texto)
    
    def calcular_regressao(self):
        """Calcula a regressao linear"""
        if not self.medias:
            QMessageBox.warning(self, "Aviso", "Por favor, calcule as estatisticas primeiro!")
            return
        
        try:
            # Obter variaveis selecionadas
            var_x = self.combo_var_x.currentText()
            var_y = self.combo_var_y.currentText()
            
            if not var_x or not var_y:
                QMessageBox.warning(self, "Aviso", "Selecione as variaveis X e Y!")
                return
            
            # Preparar dados
            self.data_x = np.array([self.medias[var_x]])
            self.data_y = np.array([self.medias[var_y]])
            self.data_x_err = np.array([self.err_est[var_x]])
            self.data_y_err = np.array([self.err_est[var_y]])
            
            # Calcular regressao
            self.slope, self.intercept, self.r_squared = RegLin(self.data_x.tolist(), self.data_y.tolist())
            
            # Mostrar resultados
            resultado = "=" * 60 + "\n"
            resultado += "REGRESSAO LINEAR CALCULADA\n"
            resultado += "=" * 60 + "\n\n"
            resultado += f"Variavel X: {var_x}\n"
            resultado += f"Variavel Y: {var_y}\n\n"
            resultado += f"Equacao: y = {self.slope:.6f}x + {self.intercept:.6f}\n\n"
            resultado += f"Coeficiente Angular (m): {self.slope:.6f}\n"
            resultado += f"Coeficiente Linear (b): {self.intercept:.6f}\n"
            resultado += f"R2 (Coeficiente de Determinacao): {self.r_squared:.6f}\n\n"
            
            # Interpretar R2
            if self.r_squared > 0.95:
                resultado += "✓ Excelente ajuste (R2 > 0.95)\n"
            elif self.r_squared > 0.85:
                resultado += "✓ Bom ajuste (R2 > 0.85)\n"
            elif self.r_squared > 0.70:
                resultado += "⚠️ Ajuste moderado (R2 > 0.70)\n"
            else:
                resultado += "⚠️ Ajuste fraco (R2 < 0.70)\n"
            
            resultado += "\n⚠️ Clique em 'Plotar Grafico' para visualizar."
            
            self.texto_resultados.setText(resultado)
            
            # Habilitar botao de plotar
            self.btn_plotar.setEnabled(True)
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao calcular regressao:\n{str(e)}")
            self.texto_resultados.setText(f"❌ Erro ao calcular regressao:\n{str(e)}")
    
    def plotar_grafico(self):
        """Plota o grafico com regressao linear"""
        if self.data_x is None or self.data_y is None:
            QMessageBox.warning(self, "Aviso", "Por favor, calcule a regressao primeiro!")
            return
        
        try:
            # Limpar canvas
            self.canvas.axes.clear()
            
            # Plotar pontos com barras de erro
            self.canvas.axes.errorbar(
                self.data_x, self.data_y,
                xerr=self.data_x_err,
                yerr=self.data_y_err,
                fmt='o',
                color='red',
                ecolor='darkred',
                capsize=5,
                markersize=8,
                label='Dados experimentais',
                zorder=5
            )
            
            # Plotar reta de regressao
            x_fit = np.linspace(self.data_x.min() - 0.05*abs(self.data_x.min()), 
                               self.data_x.max() + 0.05*abs(self.data_x.max()), 500)
            y_fit = self.slope * x_fit + self.intercept
            
            self.canvas.axes.plot(
                x_fit, y_fit,
                color='blue',
                linewidth=2,
                label=f'y = {self.slope:.3f}x + {self.intercept:.3f}\nR2 = {self.r_squared:.4f}',
                zorder=3
            )
            
            # Configuracoes do grafico
            self.canvas.axes.set_xlabel(self.entrada_x.text(), fontsize=12)
            self.canvas.axes.set_ylabel(self.entrada_y.text(), fontsize=12)
            self.canvas.axes.set_title(self.entrada_titulo.text(), fontsize=14, fontweight='bold')
            self.canvas.axes.legend(loc='best', fontsize=10)
            self.canvas.axes.grid(True, alpha=0.3, linestyle='--')
            
            # Ajustar layout
            self.canvas.fig.tight_layout()
            self.canvas.draw()
            
            self.texto_resultados.append("\n✓ Grafico plotado com sucesso!")
            
            # Mudar para tab do grafico
            self.tabs.setCurrentIndex(0)
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao plotar grafico:\n{str(e)}")
            self.texto_resultados.setText(f"❌ Erro ao plotar grafico:\n{str(e)}")
    
    def limpar_tudo(self):
        """Limpa todos os dados e reinicia a interface"""
        resposta = QMessageBox.question(
            self,
            "Confirmar",
            "Deseja limpar todos os dados?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if resposta == QMessageBox.StandardButton.Yes:
            # Resetar variaveis
            self.dados_excel = None
            self.medias = {}
            self.err_est = {}
            self.err_instr = {}
            self.data_x = None
            self.data_y = None
            self.data_x_err = None
            self.data_y_err = None
            self.slope = None
            self.intercept = None
            self.r_squared = None
            self.caminho_arquivo = None
            
            # Limpar interface
            self.label_arquivo.setText("Nenhum arquivo carregado")
            self.texto_resultados.clear()
            self.texto_estatisticas.clear()
            self.combo_var_x.clear()
            self.combo_var_y.clear()
            self.tabela_dados.clear()
            self.tabela_dados.setRowCount(0)
            self.tabela_dados.setColumnCount(0)
            
            # Desabilitar botoes
            self.btn_calcular.setEnabled(False)
            self.btn_regressao.setEnabled(False)
            self.btn_plotar.setEnabled(False)
            
            # Plotar grid inicial
            self.plotar_grid_inicial()
            
            self.texto_resultados.setText("✓ Interface reiniciada. Carregue um novo arquivo para comecar.")


def iniciar_interface():
    """Funcao para iniciar a aplicacao"""
    app = QApplication(sys.argv)
    
    # Configurar estilo (opcional)
    app.setStyle('Fusion')
    
    janela = InterfaceRegressaoLinear()
    janela.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    iniciar_interface()
