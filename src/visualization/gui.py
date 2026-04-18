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

from src.core import calcular_estatisticas, RegLin
from src.core.statistics import particionar


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
        self.dados_excel    = None
        self.dados_brutos   = {}
        self.medias         = {}
        self.err_est        = {}
        self.err_total      = {}
        self.err_instr      = {}
        self.data_x         = None
        self.data_y         = None
        self.data_x_err     = None
        self.data_y_err     = None
        self.slope          = None
        self.intercept      = None
        self.r_squared      = None
        self.caminho_arquivo = None

        self.setup_ui()

    # ------------------------------------------------------------------ #
    #  Construcao da UI                                                   #
    # ------------------------------------------------------------------ #

    def setup_ui(self):
        """Configura a interface do usuario"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # ---------- PAINEL ESQUERDO ----------
        painel_esquerdo = QWidget()
        layout_esquerdo = QVBoxLayout(painel_esquerdo)

        titulo_label = QLabel("📊 SCalc - Analise de Regressao")
        titulo_font = QFont()
        titulo_font.setPointSize(14)
        titulo_font.setBold(True)
        titulo_label.setFont(titulo_font)
        titulo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_esquerdo.addWidget(titulo_label)

        # 1. Carregar Arquivo
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

        # 2. Selecionar Variaveis  (vem antes de Configurar Eixos;
        #    os labels sao preenchidos automaticamente ao selecionar)
        grupo_variaveis = QGroupBox("2. Selecionar Variáveis")
        layout_variaveis = QVBoxLayout()
        layout_variaveis.addWidget(QLabel("Variável X (independente):"))
        self.combo_var_x = QComboBox()
        self.combo_var_x.setEnabled(False)
        layout_variaveis.addWidget(self.combo_var_x)
        layout_variaveis.addWidget(QLabel("Variável Y (dependente):"))
        self.combo_var_y = QComboBox()
        self.combo_var_y.setEnabled(False)
        layout_variaveis.addWidget(self.combo_var_y)
        # sinais: auto-fill de labels + reset de regressao
        self.combo_var_x.currentTextChanged.connect(self._on_var_x_changed)
        self.combo_var_y.currentTextChanged.connect(self._on_var_y_changed)
        grupo_variaveis.setLayout(layout_variaveis)
        layout_esquerdo.addWidget(grupo_variaveis)

        # 3. Configurar Eixos  (agora vem DEPOIS da selecao de variaveis;
        #    os campos sao pre-preenchidos com os nomes dos prefixos)
        grupo_eixos = QGroupBox("3. Configurar Eixos")
        layout_eixos = QVBoxLayout()
        layout_eixos.addWidget(QLabel("Label do Eixo X:"))
        self.entrada_x = QLineEdit("x")
        layout_eixos.addWidget(self.entrada_x)
        layout_eixos.addWidget(QLabel("Label do Eixo Y:"))
        self.entrada_y = QLineEdit("y")
        layout_eixos.addWidget(self.entrada_y)
        layout_eixos.addWidget(QLabel("Título do Gráfico:"))
        self.entrada_titulo = QLineEdit("Gráfico Estatístico")
        layout_eixos.addWidget(self.entrada_titulo)
        grupo_eixos.setLayout(layout_eixos)
        layout_esquerdo.addWidget(grupo_eixos)

        # 4. Acoes
        grupo_acoes = QGroupBox("4. Ações")
        layout_acoes = QVBoxLayout()

        self.btn_calcular = QPushButton("🔢 Calcular Estatísticas")
        self.btn_calcular.clicked.connect(self.calcular_estatisticas)
        self.btn_calcular.setEnabled(False)
        layout_acoes.addWidget(self.btn_calcular)

        self.btn_regressao = QPushButton("📈 Calcular Regressão Linear")
        self.btn_regressao.clicked.connect(self.calcular_regressao)
        self.btn_regressao.setEnabled(False)
        layout_acoes.addWidget(self.btn_regressao)

        # Botao unificado: plota pontos se so estatisticas calculadas,
        # plota pontos + reta se regressao ja calculada
        self.btn_plotar = QPushButton("🎨 Plotar Gráfico")
        self.btn_plotar.clicked.connect(self.plotar_grafico)
        self.btn_plotar.setEnabled(False)
        layout_acoes.addWidget(self.btn_plotar)

        btn_limpar = QPushButton("🗑️ Limpar Tudo")
        btn_limpar.clicked.connect(self.limpar_tudo)
        layout_acoes.addWidget(btn_limpar)

        grupo_acoes.setLayout(layout_acoes)
        layout_esquerdo.addWidget(grupo_acoes)

        # Label de status (substitui mensagens dentro de QTextEdit)
        self.status_label = QLabel("Carregue um arquivo Excel para começar.")
        self.status_label.setWordWrap(True)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_esquerdo.addWidget(self.status_label)
        self._set_status("Carregue um arquivo Excel para começar.", "info")

        # Area de Resultados (apenas resultados numericos: regressao)
        grupo_resultados = QGroupBox("📋 Resultados")
        layout_resultados = QVBoxLayout()
        self.texto_resultados = QTextEdit()
        self.texto_resultados.setReadOnly(True)
        self.texto_resultados.setMaximumHeight(200)
        layout_resultados.addWidget(self.texto_resultados)
        grupo_resultados.setLayout(layout_resultados)
        layout_esquerdo.addWidget(grupo_resultados)

        layout_esquerdo.addStretch()

        # ---------- PAINEL DIREITO ----------
        painel_direito = QWidget()
        layout_direito = QVBoxLayout(painel_direito)

        self.tabs = QTabWidget()

        # Tab Grafico
        tab_grafico = QWidget()
        layout_tab_grafico = QVBoxLayout(tab_grafico)
        self.canvas = MplCanvas(self, width=10, height=8, dpi=100)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout_tab_grafico.addWidget(self.toolbar)
        layout_tab_grafico.addWidget(self.canvas)
        self.tabs.addTab(tab_grafico, "📊 Gráfico")

        # Tab Dados
        tab_dados = QWidget()
        layout_tab_dados = QVBoxLayout(tab_dados)
        self.tabela_dados = QTableWidget()
        layout_tab_dados.addWidget(self.tabela_dados)
        self.tabs.addTab(tab_dados, "📄 Dados")

        # Tab Estatisticas Detalhadas
        tab_estatisticas = QWidget()
        layout_tab_estatisticas = QVBoxLayout(tab_estatisticas)
        self.texto_estatisticas = QTextEdit()
        self.texto_estatisticas.setReadOnly(True)
        layout_tab_estatisticas.addWidget(self.texto_estatisticas)
        self.tabs.addTab(tab_estatisticas, "📈 Estatísticas")

        layout_direito.addWidget(self.tabs)

        splitter.addWidget(painel_esquerdo)
        splitter.addWidget(painel_direito)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)

        main_layout.addWidget(splitter)

        self.plotar_grid_inicial()

    # ------------------------------------------------------------------ #
    #  Helpers: status, extracao de dados, reset de estado               #
    # ------------------------------------------------------------------ #

    def _set_status(self, mensagem: str, nivel: str = "info"):
        """Atualiza o label de status com cor baseada no nivel.

        Niveis:
            'info'  - azul  (instrucao neutra)
            'ok'    - verde (acao concluida com sucesso)
            'warn'  - laranja (atencao / proximo passo)
            'erro'  - vermelho (falha)
        """
        estilos = {
            "info": "color:#1565C0; background:#E3F2FD;",
            "ok":   "color:#2E7D32; background:#E8F5E9;",
            "warn": "color:#E65100; background:#FFF3E0;",
            "erro": "color:#B71C1C; background:#FFEBEE;",
        }
        base = "padding:5px; border-radius:4px; font-weight:bold;"
        self.status_label.setStyleSheet(base + estilos.get(nivel, estilos["info"]))
        self.status_label.setText(mensagem)

    def _extrair_dados_xy(self, prefixo_x: str, prefixo_y: str) -> tuple:
        """Extrai e valida arrays X e Y a partir dos dados brutos.

        Centraliza a logica que antes estava duplicada em plotar_pontos()
        e calcular_regressao().

        Returns:
            tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
                (data_x, data_y, data_x_err, data_y_err)

        Raises:
            ValueError: dados invalidos ou insuficientes.
        """
        if not prefixo_x or not prefixo_y:
            raise ValueError("Selecione as variáveis X e Y.")
        if prefixo_x == prefixo_y:
            raise ValueError("As variáveis X e Y devem ser diferentes.")
        if prefixo_x not in self.dados_brutos or prefixo_y not in self.dados_brutos:
            raise ValueError("Uma ou ambas as variáveis não foram encontradas nos dados.")

        def _processar(prefixo):
            vals, errs = [], []
            for chave in sorted(self.dados_brutos[prefixo].keys()):
                valores = self.dados_brutos[prefixo][chave]
                if valores:
                    vals.append(sum(valores) / len(valores))
                    errs.append(self.err_total.get(chave, 0.0))
            return vals, errs

        x_vals, x_errs = _processar(prefixo_x)
        y_vals, y_errs = _processar(prefixo_y)

        if len(x_vals) < 2 or len(y_vals) < 2:
            raise ValueError("Dados insuficientes (minimo 2 iteracoes por variavel).")
        if len(x_vals) != len(y_vals):
            raise ValueError(
                f"Variaveis com tamanhos diferentes: X={len(x_vals)}, Y={len(y_vals)}"
            )

        return (
            np.array(x_vals), np.array(y_vals),
            np.array(x_errs), np.array(y_errs),
        )

    def _resetar_estado_regressao(self):
        """Invalida resultados de regressao quando variaveis mudam.

        Garante que btn_plotar nao use uma reta calculada para um par de
        variaveis diferente do par atualmente selecionado.
        """
        self.slope     = None
        self.intercept = None
        self.r_squared = None
        self.data_x    = None
        self.data_y    = None
        self.data_x_err = None
        self.data_y_err = None
        self.texto_resultados.clear()
        # btn_regressao fica habilitado se ha estatisticas; btn_plotar idem
        tem_stats = bool(self.medias)
        self.btn_regressao.setEnabled(tem_stats)
        self.btn_plotar.setEnabled(tem_stats)

    def _on_var_x_changed(self, texto: str):
        """Auto-preenche label do eixo X e reseta regressao."""
        if texto:
            self.entrada_x.setText(texto)
        self._resetar_estado_regressao()

    def _on_var_y_changed(self, texto: str):
        """Auto-preenche label do eixo Y e reseta regressao."""
        if texto:
            self.entrada_y.setText(texto)
        self._resetar_estado_regressao()

    # ------------------------------------------------------------------ #
    #  Acoes principais                                                   #
    # ------------------------------------------------------------------ #

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
            self, "Selecionar Arquivo Excel", "",
            "Arquivos Excel (*.xlsx *.xls)"
        )
        if not caminho:
            return

        try:
            self.caminho_arquivo = caminho
            self.dados_excel = pd.read_excel(caminho)
            # Pega apenas o nome do arquivo (compativel com / e \)
            nome = caminho.replace('\\', '/').split('/')[-1]
            self.label_arquivo.setText(f"✓ {nome}")
            self.mostrar_dados_tabela()
            self.btn_calcular.setEnabled(True)
            self._set_status("Arquivo carregado. Clique em 'Calcular Estatísticas'.", "warn")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar arquivo:\n{str(e)}")
            self._set_status("Erro ao carregar arquivo.", "erro")

    def mostrar_dados_tabela(self):
        """Mostra os dados carregados na tab Dados"""
        if self.dados_excel is None:
            return
        df = self.dados_excel
        self.tabela_dados.setRowCount(len(df))
        self.tabela_dados.setColumnCount(len(df.columns))
        self.tabela_dados.setHorizontalHeaderLabels([str(c) for c in df.columns])
        for i in range(len(df)):
            for j in range(len(df.columns)):
                valor = df.iloc[i, j]
                if pd.notna(valor):
                    self.tabela_dados.setItem(i, j, QTableWidgetItem(str(valor)))
        self.tabela_dados.resizeColumnsToContents()

    def calcular_estatisticas(self):
        """Calcula medias e erros estatisticos"""
        if self.dados_excel is None:
            QMessageBox.warning(self, "Aviso", "Carregue um arquivo primeiro!")
            return

        try:
            self.dados_brutos, self.err_instr, _ = particionar(self.dados_excel)
            resultado_stats = calcular_estatisticas(self.dados_excel)

            self.medias    = dict(zip(resultado_stats['Dados'], resultado_stats['Media']))
            self.err_est   = dict(zip(resultado_stats['Dados'], resultado_stats['S_err']))
            self.err_total = dict(zip(resultado_stats['Dados'], resultado_stats['T_err']))

            prefixos = sorted(self.dados_brutos.keys())

            # Bloquear sinais para nao disparar reset durante preenchimento
            self.combo_var_x.blockSignals(True)
            self.combo_var_y.blockSignals(True)

            self.combo_var_x.clear()
            self.combo_var_y.clear()
            self.combo_var_x.addItems(prefixos)
            self.combo_var_y.addItems(prefixos)

            if len(prefixos) >= 2:
                self.combo_var_x.setCurrentIndex(0)
                self.combo_var_y.setCurrentIndex(1)
                self.entrada_x.setText(prefixos[0])
                self.entrada_y.setText(prefixos[1])

            self.combo_var_x.setEnabled(True)
            self.combo_var_y.setEnabled(True)
            self.combo_var_x.blockSignals(False)
            self.combo_var_y.blockSignals(False)

            self.mostrar_estatisticas_detalhadas()
            self.btn_regressao.setEnabled(True)
            self.btn_plotar.setEnabled(True)
            self._set_status(
                f"Estatísticas calculadas. Variáveis: {', '.join(prefixos)}.", "ok"
            )

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao calcular estatísticas:\n{str(e)}")
            self._set_status("Erro ao calcular estatísticas.", "erro")

    def mostrar_estatisticas_detalhadas(self):
        """Mostra estatisticas detalhadas na tab Estatisticas"""
        if not self.medias or not self.dados_brutos:
            return

        texto = "=" * 60 + "\n"
        texto += "ESTATÍSTICAS DETALHADAS\n"
        texto += "=" * 60 + "\n\n"

        for prefixo in sorted(self.dados_brutos.keys()):
            texto += f"Variável: {prefixo}\n"
            texto += "-" * 40 + "\n"
            for chave in sorted(self.dados_brutos[prefixo].keys()):
                valores = self.dados_brutos[prefixo][chave]
                if valores:
                    media = sum(valores) / len(valores)
                    erro_total = self.err_total.get(chave, 0.0)
                    texto += (
                        f"  {chave}: média = {media:.6f}, "
                        f"erro total = {erro_total:.6f}, "
                        f"n = {len(valores)}\n"
                    )
            texto += "\n"

        self.texto_estatisticas.setText(texto)

    def calcular_regressao(self):
        """Calcula a regressao linear"""
        if not self.medias or not self.dados_brutos:
            QMessageBox.warning(self, "Aviso", "Calcule as estatísticas primeiro!")
            return

        try:
            prefixo_x = self.combo_var_x.currentText()
            prefixo_y = self.combo_var_y.currentText()

            self.data_x, self.data_y, self.data_x_err, self.data_y_err = \
                self._extrair_dados_xy(prefixo_x, prefixo_y)

            self.slope, self.intercept, self.r_squared = \
                RegLin(self.data_x.tolist(), self.data_y.tolist())

            resultado  = "=" * 50 + "\n"
            resultado += "REGRESSÃO LINEAR\n"
            resultado += "=" * 50 + "\n\n"
            resultado += f"X: {prefixo_x}   |   Y: {prefixo_y}\n"
            resultado += f"Iterações: {len(self.data_x)}\n\n"
            resultado += f"y = {self.slope:.6f}·x + {self.intercept:.6f}\n\n"
            resultado += f"  m (coef. angular): {self.slope:.6f}\n"
            resultado += f"  b (coef. linear):  {self.intercept:.6f}\n"
            resultado += f"  R²:                {self.r_squared:.6f}\n\n"

            if self.r_squared > 0.95:
                resultado += "✓ Excelente ajuste (R² > 0,95)\n"
                nivel = "ok"
            elif self.r_squared > 0.85:
                resultado += "✓ Bom ajuste (R² > 0,85)\n"
                nivel = "ok"
            elif self.r_squared > 0.70:
                resultado += "⚠ Ajuste moderado (R² > 0,70)\n"
                nivel = "warn"
            else:
                resultado += "⚠ Ajuste fraco (R² < 0,70)\n"
                nivel = "warn"

            self.texto_resultados.setText(resultado)
            self._set_status("Regressão calculada. Clique em 'Plotar Gráfico'.", nivel)

        except ValueError as e:
            QMessageBox.warning(self, "Aviso", str(e))
            self._set_status(str(e), "erro")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao calcular regressão:\n{str(e)}")
            self._set_status("Erro ao calcular regressão.", "erro")

    def plotar_grafico(self):
        """Plota pontos com barras de erro.

        Comportamento adaptativo:
        - Se a regressao foi calculada: exibe pontos (vermelho) + reta de ajuste.
        - Se apenas as estatisticas foram calculadas: exibe so os pontos (azul).
        O botao 'Plotar Grafico' cobre os dois casos, eliminando a necessidade
        de botoes separados 'Plotar Pontos' e 'Plotar Regressao'.
        """
        if not self.medias or not self.dados_brutos:
            QMessageBox.warning(self, "Aviso", "Calcule as estatísticas primeiro!")
            return

        try:
            prefixo_x = self.combo_var_x.currentText()
            prefixo_y = self.combo_var_y.currentText()

            # Usa dados ja extraidos (se regressao calculada) ou extrai agora
            if self.data_x is not None:
                data_x, data_y = self.data_x, self.data_y
                data_x_err, data_y_err = self.data_x_err, self.data_y_err
            else:
                data_x, data_y, data_x_err, data_y_err = \
                    self._extrair_dados_xy(prefixo_x, prefixo_y)

            self.canvas.axes.clear()

            tem_regressao = self.slope is not None
            cor_ponto = 'red'   if tem_regressao else 'blue'
            cor_erro  = 'darkred' if tem_regressao else 'darkblue'

            self.canvas.axes.errorbar(
                data_x, data_y,
                xerr=data_x_err, yerr=data_y_err,
                fmt='o', color=cor_ponto, ecolor=cor_erro,
                capsize=5, markersize=8,
                label='Dados experimentais', zorder=5
            )

            if tem_regressao:
                x_fit = np.linspace(
                    data_x.min() - 0.05 * abs(data_x.min()),
                    data_x.max() + 0.05 * abs(data_x.max()),
                    500
                )
                y_fit = self.slope * x_fit + self.intercept
                self.canvas.axes.plot(
                    x_fit, y_fit,
                    color='blue', linewidth=2,
                    label=(
                        f'y = {self.slope:.3f}x + {self.intercept:.3f}'
                        f'\nR² = {self.r_squared:.4f}'
                    ),
                    zorder=3
                )
                titulo_plot   = self.entrada_titulo.text()
                status_msg    = "Gráfico com regressão plotado com sucesso."
            else:
                titulo_plot = f"Pontos: {prefixo_x} vs {prefixo_y}"
                status_msg  = "Pontos plotados (regressão não calculada)."

            self.canvas.axes.set_xlabel(self.entrada_x.text(), fontsize=12)
            self.canvas.axes.set_ylabel(self.entrada_y.text(), fontsize=12)
            self.canvas.axes.set_title(titulo_plot, fontsize=14, fontweight='bold')
            self.canvas.axes.legend(loc='best', fontsize=10)
            self.canvas.axes.grid(True, alpha=0.3, linestyle='--')
            self.canvas.fig.tight_layout()
            self.canvas.draw()

            self._set_status(status_msg, "ok")
            self.tabs.setCurrentIndex(0)

        except ValueError as e:
            QMessageBox.warning(self, "Aviso", str(e))
            self._set_status(str(e), "erro")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao plotar:\n{str(e)}")
            self._set_status("Erro ao plotar.", "erro")

    def limpar_tudo(self):
        """Limpa todos os dados e reinicia a interface"""
        resposta = QMessageBox.question(
            self, "Confirmar", "Deseja limpar todos os dados?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if resposta != QMessageBox.StandardButton.Yes:
            return

        # Resetar estado
        self.dados_excel     = None
        self.dados_brutos    = {}
        self.medias          = {}
        self.err_est         = {}
        self.err_total       = {}
        self.err_instr       = {}
        self.data_x          = None
        self.data_y          = None
        self.data_x_err      = None
        self.data_y_err      = None
        self.slope           = None
        self.intercept       = None
        self.r_squared       = None
        self.caminho_arquivo = None

        # Limpar widgets
        self.label_arquivo.setText("Nenhum arquivo carregado")
        self.texto_resultados.clear()
        self.texto_estatisticas.clear()

        self.combo_var_x.blockSignals(True)
        self.combo_var_y.blockSignals(True)
        self.combo_var_x.clear()
        self.combo_var_y.clear()
        self.combo_var_x.setEnabled(False)
        self.combo_var_y.setEnabled(False)
        self.combo_var_x.blockSignals(False)
        self.combo_var_y.blockSignals(False)

        self.tabela_dados.clear()
        self.tabela_dados.setRowCount(0)
        self.tabela_dados.setColumnCount(0)

        self.btn_calcular.setEnabled(False)
        self.btn_regressao.setEnabled(False)
        self.btn_plotar.setEnabled(False)

        # Restaurar defaults dos campos de texto
        self.entrada_x.setText("x")
        self.entrada_y.setText("y")
        self.entrada_titulo.setText("Gráfico Estatístico")

        self.plotar_grid_inicial()
        self._set_status("Interface reiniciada. Carregue um novo arquivo.", "info")


# ------------------------------------------------------------------ #
#  Ponto de entrada                                                   #
# ------------------------------------------------------------------ #

def iniciar_interface():
    """Funcao para iniciar a aplicacao"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    janela = InterfaceRegressaoLinear()
    janela.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    iniciar_interface()
