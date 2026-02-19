# SCalc — Especificações Técnicas

Referência técnica completa do projeto. Destinada a desenvolvedores que queiram entender, manter ou estender o SCalc.

---

## Sumário

1. [Visão geral da arquitetura](#visão-geral-da-arquitetura)
2. [Estrutura de diretórios](#estrutura-de-diretórios)
3. [Fluxo de dados](#fluxo-de-dados)
4. [Módulos em detalhe](#módulos-em-detalhe)
5. [Sistema de configuração](#sistema-de-configuração)
6. [Sistema de logging](#sistema-de-logging)
7. [Hierarquia de exceções](#hierarquia-de-exceções)
8. [Testes](#testes)
9. [Build](#build)
10. [Extensibilidade](#extensibilidade)
11. [Dependências](#dependências)

---

## Visão geral da arquitetura

O SCalc segue uma separação em três camadas. As dependências fluem apenas de cima para baixo — `core` nunca importa de `visualization`, e `utils`/`data` nunca importam de `core`.

```
┌──────────────────────────────────────────────────────┐
│                  scalc.py  (dispatcher)               │
└──────────────┬───────────────────────────┬───────────┘
               │                           │
    ┌──────────▼──────────┐   ┌────────────▼──────────┐
    │  visualization/      │   │  visualization/        │
    │    gui.py            │   │    plots.py            │
    └──────────┬───────────┘   └────────────┬──────────┘
               │                            │
    ┌──────────▼────────────────────────────▼──────────┐
    │                      core/                        │
    │        statistics.py          regression.py       │
    └──────────┬────────────────────────────────────────┘
               │
    ┌──────────▼──────────┐   ┌───────────────────────┐
    │      utils/          │   │       data/            │
    │  parsers.py          │   │     config.py          │
    │  validador.py        │   │                        │
    └──────────────────────┘   └───────────────────────┘
```

**Nota sobre importação circular:** `ValidadorDados` (em `utils/validador.py`) não é exportado pelo `utils/__init__.py`. Qualquer módulo que precise dele deve importar diretamente:

```python
from src.utils.validador import ValidadorDados  # correto
from src.utils import ValidadorDados             # causa circular import
```

O motivo é que `validador.py` importa de `core/exceptions.py`, que por sua vez está no pacote `core`. Se `utils/__init__.py` importasse `validador.py`, qualquer importação de `src.utils` antes de `src.core` estar completamente inicializado provocaria `ImportError`.

---

## Estrutura de diretórios

```
SCalc/
├── scalc.py                     # Dispatcher CLI/GUI — ponto de entrada único
├── build.py                     # Build via PyInstaller (--onefile / --onedir)
├── setup.py / setup.sh          # Instalação assistida de dependências
├── requirements.txt             # Dependências Python
│
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py          # Exporta: calcular_estatisticas, particionar,
│   │   │                        #           calcular_stats_prefixo, RegLin
│   │   ├── statistics.py        # particionar(), calcular_estatisticas(),
│   │   │                        # calcular_stats_prefixo()
│   │   ├── regression.py        # RegLin()
│   │   └── exceptions.py        # Hierarquia de exceções customizadas
│   │
│   ├── visualization/
│   │   ├── __init__.py          # Exporta: PlotarGrafico
│   │   ├── gui.py               # InterfaceRegressaoLinear (PySide6)
│   │   └── plots.py             # PlotarGrafico() para modo CLI
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   └── config.py            # Classe Config + setup_logging()
│   │
│   └── utils/
│       ├── __init__.py          # Exporta: eh_erro_instrumental,
│       │                        #           extrair_prefixo, contar
│       │                        #           (ValidadorDados não exportado aqui)
│       ├── parsers.py           # Funções de parsing de nomes de coluna
│       └── validador.py         # ValidadorDados — validação centralizada
│
├── tests/
│   ├── __init__.py
│   ├── test_statistics.py       # 20 testes: particionar + calcular_estatisticas
│   ├── test_regression.py       # 9 testes: RegLin
│   └── test_parsers.py          # 23 testes: extrair_prefixo, eh_erro_instrumental, contar
│
├── assets/
│   ├── scalc_icon.ico           # Ícone Windows (usado no build)
│   └── scalc_icon.png           # Ícone geral
│
├── examples/
│   └── gerar_dados_exemplo.py   # Gera src/data/test_table.xlsx no formato correto
│
├── documents/
│   ├── GUIA_VISUAL.md           # Manual do usuário
│   ├── PROJETO_COMPLETO.md      # Este arquivo
│   └── LICENSE                  # MIT
│
└── logs/                        # Gerado em runtime pelo setup_logging()
    └── scalc.log
```

---

## Fluxo de dados

### Modo GUI

```
arquivo.xlsx
      │
      ▼  pd.read_excel()
  pd.DataFrame
      │
      ▼  particionar(df)
  dados_brutos : dict[prefixo → dict[chave → list[float]]]
  erros_instr  : dict[prefixo → dict[chave → float]]
  dados_keys   : dict[prefixo → int]
      │
      ▼  calcular_estatisticas(df)
  pd.DataFrame ['Dados', 'Media', 'S_err', 'T_err']
      │
      ├─ popula dropdowns com os prefixos de dados_brutos
      │
      ▼  usuário seleciona prefixo_x e prefixo_y
      │
      ▼  GUI monta x, y, x_err, y_err a partir de dados_brutos
  x, y, x_err, y_err : np.ndarray
      │
      ▼  RegLin(x, y)
  slope, intercept, r_squared : float
      │
      ▼  canvas.axes.errorbar() + canvas.axes.plot()
  Gráfico interativo embutido no Qt
```

### Modo CLI

```
--arquivo <path>
      │
      ▼  ValidadorDados.validar_arquivo_excel()
      ▼  pd.read_excel()
      ▼  ValidadorDados.validar_dataframe()
      │
      ▼  particionar()
      │
      ├─ seleciona os dois primeiros prefixos por ordem alfabética
      │
      ▼  calcular_stats_prefixo() ← helper compartilhado, sem duplicação
  x_vals, x_errs, y_vals, y_errs
      │
      ▼  RegLin()
      │
      ▼  logger.info() — imprime resultados no terminal
      ▼  PlotarGrafico() — janela matplotlib bloqueante
```

---

## Módulos em detalhe

### `scalc.py` — ponto de entrada

Dispatcher puro. Analisa argumentos com `argparse` e roteia para `modo_gui()` ou `modo_cli()`.

**Argumentos CLI:**

| Argumento | Tipo | Padrão | Descrição |
|---|---|---|---|
| `--gui` | flag | — | Modo GUI (padrão quando nenhum argumento é passado) |
| `--cli` | flag | — | Ativa processamento em linha de comando |
| `--arquivo` / `-f` | `str` | — | Caminho para o `.xlsx` (obrigatório no modo CLI) |
| `--x-label` | `str` | `"x"` | Rótulo do eixo X |
| `--y-label` | `str` | `"y"` | Rótulo do eixo Y |
| `--titulo` | `str` | `"Gráfico..."` | Título do gráfico |

`setup_logging(nivel='INFO')` é chamado na entrada de `main()` antes de qualquer processamento.

---

### `src/core/statistics.py`

Contém as três funções públicas do processamento estatístico.

---

#### `particionar(tabela: pd.DataFrame) -> tuple`

**Assinatura de retorno:**
```python
tuple[
    dict[str, dict[str, list[float]]],  # dados_brutos
    dict[str, dict[str, float]],         # erros_instrumentais
    dict[str, int]                        # dados_keys
]
```

**Algoritmo — duas passagens sobre as colunas:**

A função faz duas iterações independentes pelas colunas do DataFrame. Isso garante que a ordem das colunas no arquivo Excel não afete o resultado (a coluna `I_err` pode aparecer antes ou depois da coluna `Dados`).

**Passagem 1** — localiza a coluna de identificadores (aquela cujo nome contém `"dados"`, case-insensitive) e constrói:
- `lista_dados`: lista posicional com os identificadores em ordem de linha. Ex: `['a_1', 'a_2', 'b_1', 'b_2']`
- `dados_keys`: contagem de pontos por prefixo. Ex: `{'a': 2, 'b': 2}`

**Passagem 2** — percorre todas as colunas novamente:
- Colunas de erro (`eh_erro_instrumental() == True`): mapeadas posicionalmente sobre `lista_dados`. O valor na posição `i` da coluna de erro é associado ao identificador `lista_dados[i]`.
- Colunas numéricas (tudo que não é `"dados"` nem erro): cada coluna é uma repetição. Os valores são agrupados pelo identificador posicional correspondente em `lista_dados`, respeitando `NaN` intercalados via iteração pelo índice original do DataFrame.

**Resultado final:**
```python
dados_brutos = {
    'a': {'a_1': [1.0, 1.1, 0.9],  'a_2': [2.0, 2.1, 1.9]},
    'b': {'b_1': [2.0, 2.1, 1.9],  'b_2': [4.0, 4.1, 3.9]},
}
erros_instrumentais = {
    'a': {'a_1': 0.10, 'a_2': 0.10},
    'b': {'b_1': 0.20, 'b_2': 0.20},
}
dados_keys = {'a': 2, 'b': 2}
```

**Raises:**
- `DadosInvalidosException` — DataFrame vazio, só NaN, ou nenhum dado numérico válido após o particionamento
- `ColunasInvalidasException` — todas as colunas foram classificadas como erro instrumental

---

#### `calcular_stats_prefixo(dados_por_chave, erros_por_chave) -> tuple`

Helper exportado que centraliza o cálculo de médias e erros para um único grupo. Usado tanto por `calcular_estatisticas()` quanto pelo `modo_cli()` em `scalc.py`, eliminando a duplicação de lógica que existia anteriormente.

```python
def calcular_stats_prefixo(
    dados_por_chave: dict[str, list[float]],
    erros_por_chave: dict[str, float],
) -> tuple[list[float], list[float]]:
    # Retorna (medias, erros_totais) em ordem alfabética de chaves
```

**Fórmulas:**
```
n     = len(valores)
media = sum(valores) / n

S_err = sqrt(Σ(xᵢ - media)² / (n-1)) / sqrt(n)   se n > 1
      = 0.0                                          se n == 1

# Propagação quadrática de erros
T_err = sqrt(S_err² + I_err²)
```

O denominador `n-1` é a correção de Bessel — produz o desvio padrão amostral (estimativa não-viesada da população), e dividir por `sqrt(n)` converte para erro padrão da média.

---

#### `calcular_estatisticas(tabela: pd.DataFrame) -> pd.DataFrame`

Chama `particionar()` e agrega todos os grupos em um DataFrame de resultados.

**Colunas de saída:**

| Coluna | Tipo | Descrição |
|---|---|---|
| `'Dados'` | `str` | Identificador do ponto (ex: `'a_1'`) |
| `'Media'` | `float` | Média aritmética das repetições |
| `'S_err'` | `float` | Erro estatístico (erro padrão da média) |
| `'T_err'` | `float` | Erro total por propagação quadrática |

**Raises:**
- `DadosInvalidosException` — DataFrame inválido ou sem dados numéricos
- `DadosInsuficientesException` — zero medições após o particionamento

---

### `src/core/regression.py`

#### `RegLin(x, y) -> tuple[float, float, float]`

Wrapper sobre `scipy.stats.linregress`. Aceita listas Python ou `np.ndarray`.

```python
slope, intercept, r_squared = RegLin(x, y)
```

`r_squared` é calculado como `rvalue ** 2`, onde `rvalue` é o coeficiente de correlação de Pearson. `linregress` retorna cinco valores — apenas os três primeiros são usados (`slope`, `intercept`, `rvalue`).

---

### `src/utils/parsers.py`

Funções puras de parsing de nomes de coluna. Sem dependências internas ao projeto.

#### `extrair_prefixo(nome: Any) -> str | None`

Extrai a sequência alfabética inicial via `re.match(r'^([a-zA-Z]+)', nome.strip())`.

```python
extrair_prefixo('a_1')          # → 'a'
extrair_prefixo('temperatura2') # → 'temperatura'
extrair_prefixo('123')          # → None
extrair_prefixo(None)           # → None  (guarda com isinstance)
```

#### `eh_erro_instrumental(nome_coluna: Any) -> bool`

Detecta colunas de erro instrumental com duas condições simultâneas:

- **Indicador de ERRO por substring** (case-insensitive): a string contém `'err'`, `'error'` ou `'erro'` em qualquer posição. Substring é usada deliberadamente para capturar padrões concatenados como `'xerr'` ou `'ierr'`.

- **Indicador de INSTRUMENTAL por token exato**: após split por `[_\-\s]+`, algum token resultante é exatamente um de `{'i', 'instr', 'ins', 'instrumental', 'instrument'}`. Token exato (não substring) evita falsos positivos pela letra `'i'` embutida em palavras como `'distancia'` ou `'medicao'`.

```python
eh_erro_instrumental('I_err')        # True  — token 'i' + substring 'err'
eh_erro_instrumental('xerr_instr')   # True  — token 'instr' + substring 'xerr'
eh_erro_instrumental('distancia_err')# False — 'distancia' não é token instr
eh_erro_instrumental('x_err')        # False — 'x' não é token instr
```

#### `contar(prefixo: str, lista: list) -> int`

Conta itens que começam com `prefixo` seguido obrigatoriamente de um separador (`_`, ` `, `-`, `\n`). O separador é obrigatório para que prefixos não sejam encontrados como substrings de nomes mais longos.

```python
contar('a',    ['a_1', 'a_2', 'temperatura_1'])  # → 2  (não conta 'temperatura_1')
contar('temp', ['temperatura_1', 'temp_1'])       # → 1  (não conta 'temperatura_1')
```

---

### `src/utils/validador.py`

Classe estática `ValidadorDados` com métodos de validação centralizados. Importação sempre direta — nunca via `src.utils`:

```python
from src.utils.validador import ValidadorDados
```

| Método | Valida | Raises |
|---|---|---|
| `validar_dataframe(df, nome)` | `isinstance`, não vazio, tem colunas | `DadosInvalidosException` |
| `validar_arquivo_excel(caminho)` | existência, extensão `.xlsx`/`.xls`, tamanho ≤ `MAX_TAMANHO_ARQUIVO_MB` | `ArquivoInvalidoException` |
| `validar_dados_numericos(serie, nome)` | converte com `pd.to_numeric(errors='coerce')`, verifica se não é tudo NaN | `DadosNaoNumericosException` |
| `validar_medicoes_minimas(dados, min)` | total de medições ≥ `min` | `DadosInsuficientesException` |
| `validar_tamanho_arquivo(df, ...)` | limites de linhas e colunas configurados em `Config.Validacao` | `DadosInvalidosException` |

---

### `src/data/config.py`

#### Classe `Config`

Namespace de configuração com classes internas aninhadas. Nunca instanciada — todos os atributos são de classe.

```
Config
├── APP_NAME, APP_VERSION, APP_AUTHOR, APP_DESCRIPTION
├── PROJECT_ROOT, SRC_DIR, DATA_DIR, DOCS_DIR, EXAMPLES_DIR  (Path)
│
├── Config.Plot
│   ├── STYLE = '_mpl-gallery'
│   ├── FIGURE_WIDTH = 8, FIGURE_HEIGHT = 6, FIGURE_DPI = 100
│   ├── COLOR_PONTOS = 'blue', COLOR_ERRO = 'red', COLOR_REGRESSAO = 'green'
│   ├── LINEWIDTH_REGRESSAO = 2.0, MARKERSIZE_PONTOS = 6, CAPSIZE_ERRO = 5
│   ├── DEFAULT_X_LABEL = 'x', DEFAULT_Y_LABEL = 'y'
│   └── FORMATOS_EXPORTACAO = ['png', 'pdf', 'svg', 'jpg', 'eps']
│
├── Config.Estatistica
│   ├── R2_EXCELENTE = 0.95, R2_BOM = 0.85, R2_MODERADO = 0.70
│   ├── NIVEL_CONFIANCA = 0.95
│   ├── MIN_MEDICOES_RECOMENDADO = 3
│   └── PRECISAO_DECIMAL = 6
│
├── Config.Validacao
│   ├── MAX_TAMANHO_ARQUIVO_MB = 50
│   ├── MAX_COLUNAS = 100, MAX_LINHAS = 10000
│   └── PERMITIR_VALORES_FALTANTES = True
│
├── Config.UI
│   ├── WINDOW_WIDTH = 1400, WINDOW_HEIGHT = 900
│   ├── WINDOW_MIN_WIDTH = 1000, WINDOW_MIN_HEIGHT = 700
│   └── FONT_TITULO_SIZE, FONT_LABEL_SIZE, FONT_TEXTO_SIZE
│
└── Config.Logging
    ├── NIVEL_PADRAO = 'INFO'
    ├── FORMATO = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ├── ARQUIVO_LOG = <project_root>/logs/scalc.log
    ├── MAX_BYTES = 10 MB
    └── BACKUP_COUNT = 3
```

**Métodos de classe:**
- `Config.get_config_dict() -> dict` — snapshot das configurações para serialização
- `Config.validar_r2(r_squared: float) -> str` — classifica R² em `'excelente'`, `'bom'`, `'moderado'` ou `'fraco'`

**Aliases de compatibilidade:** o módulo expõe variáveis de nível de módulo (`PROJECT_ROOT`, `APP_NAME`, `PLOT_DPI`, etc.) que apontam para os mesmos valores de `Config`. Use `Config.*` em código novo.

---

### `src/visualization/gui.py`

#### `InterfaceRegressaoLinear(QMainWindow)`

Estado interno relevante:

| Atributo | Tipo | Descrição |
|---|---|---|
| `dados_excel` | `pd.DataFrame \| None` | DataFrame bruto do arquivo carregado |
| `dados_brutos` | `dict` | Saída de `particionar()` |
| `err_instr` | `dict` | Erros instrumentais por prefixo/chave |
| `err_total` | `dict` | Erros totais por chave |
| `data_x`, `data_y` | `np.ndarray \| None` | Médias para regressão |
| `data_x_err`, `data_y_err` | `np.ndarray \| None` | Erros totais para regressão |
| `slope`, `intercept`, `r_squared` | `float \| None` | Resultados da regressão |

**Fluxo de habilitação de botões:**

```
Inicial       │ btn_calcular=disabled  btn_regressao=disabled  btn_plotar=disabled
carregar()    │ btn_calcular=enabled
calcular()    │ btn_regressao=enabled
regressao()   │ btn_plotar=enabled
```

**`MplCanvas(FigureCanvas)`** — widget interno que embute um `Figure` do Matplotlib no Qt via `matplotlib.backends.backend_qtagg`. A barra de ferramentas é `NavigationToolbar2QT`.

**`iniciar_interface()`** — função exportada que cria `QApplication`, aplica estilo `'Fusion'`, instancia `InterfaceRegressaoLinear` e entra no loop de eventos com `sys.exit(app.exec())`.

---

### `src/visualization/plots.py`

#### `PlotarGrafico(...) -> None`

Usado exclusivamente no modo CLI. Cria figura Matplotlib bloqueante (`plt.show()`).

```python
def PlotarGrafico(
    pontos: set[tuple[float, float]],
    erros_x: list[float],
    erros_y: list[float],
    str_x: str,
    str_y: str,
    slope: float,
    intercept: float,
    titulo: str,
) -> None
```

Usa `Config.Plot.*` para estilo, tamanho, DPI e cores. A reta de regressão é desenhada via `np.arange` baseado nos extremos arredondados do conjunto de pontos.

---

## Sistema de logging

`setup_logging(nivel: str | None = None)` configura dois handlers no logger raiz:

1. **`RotatingFileHandler`** → `logs/scalc.log`, rotaciona em 10 MB, mantém 3 backups
2. **`StreamHandler`** → stdout com o mesmo formato

O diretório `logs/` é criado automaticamente. Para filtrar logs por módulo:

```python
# Silenciar statistics.py especificamente:
logging.getLogger('src.core.statistics').setLevel(logging.WARNING)
```

---

## Hierarquia de exceções

```
Exception
└── ScalcException
    ├── DadosInvalidosException       # dados malformados, tipo errado ou estrutura incorreta
    ├── DadosInsuficientesException   # quantidade insuficiente de medições
    ├── ColunasInvalidasException     # estrutura de colunas incorreta
    ├── DadosNaoNumericosException    # coluna esperada como numérica contém texto
    ├── RegressaoException            # falha interna do cálculo de regressão
    ├── ArquivoInvalidoException      # arquivo inválido, inexistente ou grande demais
    └── ConfiguracaoException         # configuração inválida (reservada para uso futuro)
```

Capture `ScalcException` para tratar qualquer erro do domínio do projeto de uma vez. Capture subclasses específicas quando o tratamento diferenciado for necessário.

---

## Testes

### Executar

```bash
# Suite completa — sempre da raiz do projeto
python -m unittest discover -s . -p "test_*.py" -v

# Suite específica
python -m unittest discover -s . -p "test_statistics.py"
python -m unittest discover -s . -p "test_regression.py"
python -m unittest discover -s . -p "test_parsers.py"
```

> **Por que `-s .` e não `-s tests/`?** O `discover` adiciona o diretório de início ao `sys.path`. Com `-s tests/`, o prefixo `src` não estaria no path e todos os `import src.*` dentro dos testes falhariam com `ModuleNotFoundError`.

### Cobertura

| Suite | Testes | Funções cobertas |
|---|---|---|
| `test_statistics.py` | 20 | `particionar`, `calcular_estatisticas`, independência de ordem de colunas |
| `test_regression.py` | 9 | `RegLin`, tipos de retorno, reta perfeita, ruído, 2 pontos, numpy |
| `test_parsers.py` | 23 | `extrair_prefixo`, `eh_erro_instrumental`, `contar`, regressões de bugs corrigidos |

### Testes de regressão de bugs corrigidos

Os testes abaixo foram adicionados especificamente para garantir que bugs corrigidos não retornem:

**`test_parsers.py :: test_letra_i_embutida_em_palavra_nao_e_token`**
Verifica que `'distancia_err'`, `'medicao_error'` e similares retornam `False`. Antes da correção, a letra `'i'` em qualquer posição da string causava falso positivo.

**`test_parsers.py :: test_nao_conta_substring_de_nome_maior`**
Verifica que `contar('temp', ['temperatura_1', 'temp_1'])` retorna `1`. Antes da correção, a última condição `startswith(prefixo + "")` causava match em substrings.

**`test_statistics.py :: test_ordem_de_colunas_nao_afeta_resultado`**
Verifica que `particionar` produz resultado idêntico com `I_err` antes ou depois de `Dados`. Antes da correção, a coluna de erro sendo processada antes da coluna de identificadores resultava em `TypeError` (lista usada como chave de dicionário) ou mapeamento silenciosamente incorreto.

**`test_statistics.py :: test_i_err_antes_de_dados_nao_crasha`**
Garante que não ocorre `TypeError` específico quando a ordem é `I_err → Dados`.

### Lacunas de cobertura

- `ValidadorDados` — testado indiretamente via `calcular_estatisticas`; sem suite dedicada
- `PlotarGrafico` — requer display gráfico
- `InterfaceRegressaoLinear` — requer `QApplication`
- `setup_logging` e `Config` — sem testes

---

## Build

```bash
python build.py -y              # onefile, sem prompt de confirmação
python build.py --onedir -y     # diretório (inicialização mais rápida)
python build.py --windowed -y   # oculta console (desabilita saída do modo CLI)
```

**Hidden imports declarados:** `scipy.stats` e seus sub-módulos são carregados dinamicamente por `linregress` e não são detectados por análise estática do PyInstaller. O mesmo vale para sub-módulos internos de `pandas._libs.tslibs.*` e para todos os módulos do projeto em `src.*`.

**`--optimize 1` e não `2`:** nível 2 remove docstrings em tempo de compilação, o que pode corromper introspecção usada por scipy e pandas em determinados contextos. Nível 1 é seguro.

**`--windowed` é opt-in:** ocultar o console no Windows silencia completamente o modo `--cli`. Por isso a flag não é aplicada por padrão.

**Ícone:** `assets/scalc_icon.ico` no Windows, `assets/scalc_icon.icns` no macOS (arquivo não incluído no repositório — o build no macOS usa ícone padrão se não encontrado).

---

## Extensibilidade

### Adicionar novo tipo de regressão

```python
# src/core/regression.py
def RegPolinomial(x, y, grau=2) -> tuple:
    """Regressão polinomial de grau n."""
    coefs = np.polyfit(x, y, grau)
    p     = np.poly1d(coefs)
    ss_res = np.sum((y - p(x)) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    return coefs, float(1 - ss_res / ss_tot)

# src/core/__init__.py
from .regression import RegLin, RegPolinomial
```

### Adicionar novo formato de entrada

```python
# src/data/readers.py  (novo arquivo)
import pandas as pd

def ler_csv(caminho: str) -> pd.DataFrame:
    """Lê CSV e converte para o formato esperado por particionar()."""
    df = pd.read_csv(caminho)
    # garantir colunas 'Dados', 'I_err', e colunas numéricas de repetição
    return df
```

Em `scalc.py`, detectar a extensão do arquivo e rotear para o leitor adequado antes de chamar `particionar`.

### Adicionar nova aba na GUI

```python
# src/visualization/gui.py — dentro de setup_ui()
tab_nova   = QWidget()
layout_tab = QVBoxLayout(tab_nova)
# adicionar widgets ao layout
self.tabs.addTab(tab_nova, "📊 Nova Aba")
```

### Adicionar novo método de validação

```python
# src/utils/validador.py — dentro da classe ValidadorDados
@staticmethod
def validar_grupos_suficientes(dados_brutos: dict, minimo: int = 2) -> None:
    if len(dados_brutos) < minimo:
        raise DadosInsuficientesException(
            f"Mínimo de {minimo} grupos necessário, encontrado: {len(dados_brutos)}"
        )
```

---

## Dependências

| Pacote | Versão mínima | Uso |
|---|---|---|
| `PySide6` | 6.6.0 | Interface gráfica Qt; backend do Matplotlib na GUI |
| `numpy` | 1.24.0 | Arrays numéricos; geração da reta de regressão |
| `pandas` | 2.0.0 | Leitura de Excel; manipulação tabular |
| `scipy` | 1.10.0 | `linregress` em `regression.py` |
| `matplotlib` | 3.7.0 | Plotagem CLI; canvas embutido na GUI |
| `openpyxl` | 3.1.0 | Engine de leitura/escrita de `.xlsx` pelo pandas |
| `pyinstaller` | 6.0.0+ | Build de executável (opcional; não listado por padrão) |

`scipy` é usado exclusivamente para `scipy.stats.linregress`. Se o peso da dependência for uma preocupação, a regressão pode ser reimplementada com `numpy.linalg.lstsq` ou pelas equações normais, eliminando o scipy completamente.
