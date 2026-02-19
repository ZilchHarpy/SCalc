# SCalc — Sistema de Cálculo e Análise de Regressão Linear

Ferramenta para análise estatística de dados experimentais com suporte a regressão linear, barras de erro e interface gráfica interativa.

---

## Sumário

- [Instalação](#instalação)
- [Como usar](#como-usar)
  - [Modo GUI](#modo-gui)
  - [Modo CLI](#modo-cli)
- [Modelo de tabela](#modelo-de-tabela)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Executar testes](#executar-testes)
- [Uso programático](#uso-programático)
- [Build (executável)](#build-executável)
- [Solução de problemas](#solução-de-problemas)
- [Documentação adicional](#documentação-adicional)
- [Contribuindo](#contribuindo)
- [Licença](#licença)
- [Autores](#autores)
- [Suporte](#suporte)

---

## Instalação

### Pré-requisitos

- Python 3.10 ou superior
- pip

### 1. Ambiente virtual (recomendado)

```bash
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 2. Dependências Python

```bash
pip install -r requirements.txt
```

### 3. Dependências do sistema (somente Linux)

O PySide6 depende de bibliotecas gráficas do sistema que não são instaladas pelo pip. Execute o comando correspondente à sua distribuição:

**Ubuntu / Debian**
```bash
sudo apt-get update && sudo apt-get install -y \
    libxcb-cursor0 libxcb-xinerama0 libxcb-xkb1 libxkbcommon-x11-0
```

**Fedora / RHEL**
```bash
sudo dnf install -y libxcb xcb-util-cursor libxkbcommon-x11
```

**Arch Linux**
```bash
sudo pacman -Syu --noconfirm libxcb xcb-util-cursor libxkbcommon-x11
```

> Windows e macOS não exigem etapas adicionais.

### 4. Setup assistido (alternativa)

O script `setup.py` detecta o sistema operacional, verifica as dependências e instala o que estiver faltando:

```bash
python setup.py
```

---

## Como usar

### Modo GUI

Inicia a interface gráfica (comportamento padrão quando nenhum argumento é passado):

```bash
python scalc.py
# equivalente a:
python scalc.py --gui
```

**Fluxo de uso na interface:**

1. **Carregar arquivo** — clique em *Selecionar Arquivo Excel* e escolha um `.xlsx`.
2. **Calcular estatísticas** — clique em *Calcular Estatísticas*. O programa particiona as colunas, calcula médias e erros, e popula os dropdowns de variáveis.
3. **Selecionar variáveis** — escolha qual variável será o eixo X (independente) e qual será o eixo Y (dependente).
4. **Calcular regressão** — clique em *Calcular Regressão Linear* para obter a equação `y = mx + b` e o R².
5. **Plotar gráfico** — clique em *Plotar Gráfico* para exibir o diagrama de dispersão com barras de erro e a reta ajustada.

A interface possui três abas no painel direito:

| Aba | Conteúdo |
|---|---|
| **Gráfico** | Diagrama de dispersão com reta de regressão e barra de ferramentas do Matplotlib (zoom, pan, exportar) |
| **Dados** | Tabela com os dados brutos do arquivo carregado |
| **Estatísticas** | Médias, erros estatísticos e erros totais por variável |

---

### Modo CLI

Processa um arquivo sem abrir a interface gráfica. Útil para scripts, notebooks ou automação.

```bash
python scalc.py --cli --arquivo <caminho_para_arquivo.xlsx>
```

**Parâmetros disponíveis:**

| Argumento | Alias | Descrição | Padrão |
|---|---|---|---|
| `--cli` | — | Ativa o modo linha de comando | — |
| `--arquivo` | `-f` | Caminho para o arquivo Excel | *(obrigatório no modo CLI)* |
| `--x-label` | — | Rótulo do eixo X | `"x"` |
| `--y-label` | — | Rótulo do eixo Y | `"y"` |
| `--titulo` | — | Título do gráfico | `"Gráfico de Dispersão com Regressão Linear"` |

**Exemplo completo:**

```bash
python scalc.py --cli \
    --arquivo dados/experimento.xlsx \
    --x-label "Tempo (s)" \
    --y-label "Deslocamento (m)" \
    --titulo "Cinemática — Experimento 1"
```

O programa imprime no terminal as médias, erros e os coeficientes da regressão, e em seguida exibe o gráfico via Matplotlib.

---

## Modelo de tabela

O SCalc espera um arquivo Excel com um formato específico. Abaixo está a estrutura esperada e as regras de nomenclatura.

### Estrutura esperada

| Dados | I_err | 1 | 2 | 3 |
|-------|---|---|---|-------|
| a\_1  | 0.05 | 1.2 | 1.3 | 1.1 |
| a\_2  | 0.05 | 2.3 | 2.4 | 2.2 |
| a\_3  | 0.05 | 3.5 | 3.6 | 3.4 |
| b\_1  | 0.10 | 2.4 | 2.5 | 2.3 |
| b\_2  | 0.10 | 4.6 | 4.8 | 4.5 |
| b\_3  | 0.10 | 7.0 | 7.1 | 6.9 |

### Regras de nomenclatura

**Coluna `Dados`** — lista os identificadores de cada ponto. O formato é `<prefixo>_<iteração>`, onde o prefixo agrupa pontos de uma mesma variável física. Exemplos válidos: `a_1`, `temp_2`, `pressao_3`.

**Colunas numéricas (`1`, `2`, `3`, …)** — cada coluna representa uma repetição da medição. O SCalc usa todas as repetições disponíveis por linha para calcular a média e o erro estatístico (desvio padrão da média).

**Coluna de erro instrumental (`I_err`)** — contém o erro do instrumento de medição para cada ponto. O nome deve conter `err` (ou `error` / `erro`) **e** alguma variante de `i` / `instr` / `instrumental`. Exemplos válidos: `I_err`, `i_error`, `xerr_instr`, `instr_err`. A detecção é insensível a maiúsculas.

### Cálculo dos erros

O programa propaga os erros de forma quadrática:

```
Erro estatístico  = desvio_padrão / √n
Erro total        = √(erro_estatístico² + erro_instrumental²)
```

### Notas

- Células vazias em colunas numéricas são ignoradas — repetições podem variar por ponto.
- Pelo menos dois grupos (prefixos distintos) são necessários para a regressão linear.
- Todos os grupos usados na regressão devem ter o mesmo número de pontos (mesma quantidade de identificadores `<prefixo>_<n>`).

---

## Estrutura do projeto

```
SCalc/
├── scalc.py            # Ponto de entrada — decide GUI ou CLI
├── build.py            # Script de build com PyInstaller
├── setup.py            # Setup assistido de dependências
├── requirements.txt    # Dependências Python
│
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── statistics.py   # particionar(), calcular_estatisticas()
│   │   ├── regression.py   # RegLin()
│   │   └── exceptions.py   # Exceções customizadas
│   │
│   ├── visualization/
│   │   ├── __init__.py
│   │   ├── gui.py          # Interface PySide6
│   │   └── plots.py        # PlotarGrafico() para o modo CLI
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   ├── config.py       # Configurações globais (Config)
│   │   └── test_table.xlsx # Tabela de exemplo
│   │
│   └── utils/
│       ├── __init__.py
│       ├── parsers.py      # extrair_prefixo(), eh_erro_instrumental()
│       └── validador.py    # ValidadorDados
│
├── tests/
│   ├── __init__.py
│   ├── test_statistics.py
│   ├── test_regression.py
│   └── test_parsers.py
│
├── assets/
│   ├── scalc_icon.ico
│   └── scalc_icon.png
│
├── examples/
│   └── gerar_dados_exemplo.py
│
├── documents/
│   ├── GUIA_VISUAL.md
│   ├── PROJETO_COMPLETO.md
│   └── LICENSE
│
└── logs/               # Gerado automaticamente em tempo de execução
```

---

## Executar testes

Os testes usam o módulo `unittest` da biblioteca padrão do Python. Execute a partir da raiz do projeto:

```bash
# Todos os testes (recomendado — garante que o sys.path está correto)
python -m unittest discover -s . -p "test_*.py" -v

# Suite específica
python -m unittest discover -s . -p "test_statistics.py"
python -m unittest discover -s . -p "test_regression.py"
python -m unittest discover -s . -p "test_parsers.py"
```

**Cobertura por arquivo:**

| Arquivo | Testes | O que cobre |
|---|---|---|
| `test_statistics.py` | 18 | `particionar()`, `calcular_estatisticas()`, propagação de erros, NaN, exceções |
| `test_regression.py` | 7 | `RegLin()`, reta perfeita, intercepto, dados com ruído, caso mínimo (2 pontos), R² |
| `test_parsers.py` | 17 | `extrair_prefixo()`, `eh_erro_instrumental()`, `contar()`, falso positivo documentado |

---

## Uso programático

O SCalc pode ser usado como biblioteca diretamente em outros scripts Python:

```python
import pandas as pd
import numpy as np
from src.core import calcular_estatisticas, RegLin
from src.core.statistics import particionar
from src.visualization.plots import PlotarGrafico

# Carregar dados
dados = pd.read_excel("src/data/test_table.xlsx")

# Calcular estatísticas — retorna um DataFrame com colunas:
# ['Dados', 'Media', 'S_err', 'T_err']
stats = calcular_estatisticas(dados)
print(stats)

# Particionar dados brutos (para extrair médias por grupo)
dados_brutos, erros_instr, dados_keys = particionar(dados)

# Montar vetores x e y a partir dos grupos de interesse
prefixo_x, prefixo_y = "a", "b"

x = [sum(v) / len(v) for v in sorted(dados_brutos[prefixo_x].values())]
y = [sum(v) / len(v) for v in sorted(dados_brutos[prefixo_y].values())]

# Regressão linear
slope, intercept, r_squared = RegLin(x, y)
print(f"y = {slope:.4f}x + {intercept:.4f}   R² = {r_squared:.4f}")

# Plotar
x_arr, y_arr = np.array(x), np.array(y)
PlotarGrafico(
    set(zip(x_arr, y_arr)),
    erros_x=[0.0] * len(x),
    erros_y=[0.0] * len(y),
    slope=slope,
    intercept=intercept,
    str_x="Variável A",
    str_y="Variável B",
    titulo="Exemplo de uso programático",
)
```

---

## Build (executável)

Para gerar um executável portável (sem precisar de Python instalado na máquina alvo), instale o PyInstaller e use `build.py`:

```bash
pip install pyinstaller

# Build padrão — arquivo único, console visível (CLI e GUI funcionais)
python build.py -y

# Build em modo diretório — pasta com múltiplos arquivos, inicia mais rápido
python build.py --onedir -y

# Build somente para GUI — oculta o console (CLI ficará silencioso)
python build.py --windowed -y
```

O executável gerado estará em `dist/SCalc` (ou `dist/SCalc.exe` no Windows).

> **Nota sobre `--windowed`:** ocultar o console é recomendado apenas se você não usa o modo CLI. Com essa flag ativa, o modo `--cli` ainda funciona tecnicamente, mas não exibe nenhuma saída no terminal.

---

## Solução de problemas

**`ModuleNotFoundError: No module named 'PySide6'`**
```bash
pip install PySide6
```

**`qt.qpa.plugin: Could not load the Qt platform plugin` (Linux)**

Instale as dependências do sistema listadas na seção [Instalação](#instalação) ou execute:
```bash
python setup.py
```

**Gráfico não aparece no modo CLI**

O Matplotlib precisa de um backend gráfico disponível. No Linux sem display (ex: SSH sem `-X`), exporte a variável:
```bash
export DISPLAY=:0
python scalc.py --cli --arquivo dados.xlsx
```
Ou use o backend `Agg` para salvar em arquivo em vez de exibir.

**`DadosInvalidosException: Mínimo de 2 grupos necessário`**

O arquivo não possui pelo menos dois prefixos distintos na coluna `Dados`. Revise a [estrutura da tabela](#modelo-de-tabela).

**`DadosInvalidosException: Grupos com tamanhos diferentes`**

Os dois prefixos selecionados para X e Y têm quantidades diferentes de pontos (ex: `a` tem 3 entradas e `b` tem 4). Todos os grupos usados na regressão devem ter o mesmo número de iterações.

**Build falha com erro de módulo não encontrado**

```bash
pip install --upgrade pyinstaller
pip install -r requirements.txt
python build.py --onedir -y   # modo onedir costuma ser mais tolerante
```

---

## Documentação adicional

- [`documents/GUIA_VISUAL.md`](documents/GUIA_VISUAL.md) — capturas de tela e guia visual passo a passo
- [`documents/PROJETO_COMPLETO.md`](documents/PROJETO_COMPLETO.md) — especificações técnicas detalhadas
- [`examples/gerar_dados_exemplo.py`](examples/gerar_dados_exemplo.py) — script para gerar tabelas de exemplo

---

## Contribuindo

Contribuições são bem-vindas. Para propor melhorias:

1. Faça um fork do repositório
2. Crie uma branch descritiva: `git checkout -b feature/nome-da-feature`
3. Implemente as mudanças com testes correspondentes
4. Abra um Pull Request descrevendo o que foi alterado e por quê

Para reportar bugs ou sugerir funcionalidades, abra uma [issue](https://github.com/ZilchHarpy/SCalc/issues).

---

## Licença

Este projeto está licenciado sob a licença MIT. Veja [`documents/LICENSE`](documents/LICENSE) para o texto completo.

---

## Autores

**Caio Aquilino Merino**
- GitHub: [@ZilchHarpy](https://github.com/ZilchHarpy)
- Email: caioaquilinomerino@gmail.com

---

## Suporte

- **Bugs e perguntas:** abra uma [issue no GitHub](https://github.com/ZilchHarpy/SCalc/issues)
- **Contato direto:** caioaquilinomerino@gmail.com
