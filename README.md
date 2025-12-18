# SCalc - Sistema de Cálculo e Análise de Regressão Linear

Sistema completo para análise estatística e regressão linear com interface gráfica intuitiva.

## 📋 Características

- ✅ Interface gráfica moderna com PySide6
- ✅ Visualização interativa com Matplotlib
- ✅ Cálculo automático de médias e erros estatísticos
- ✅ Regressão linear com coeficiente de determinação (R²)
- ✅ Gráficos com barras de erro
- ✅ Exportação de gráficos (PNG, PDF, SVG)
- ✅ Modo CLI para processamento em lote
- ✅ Suporte a arquivos Excel (.xlsx, .xls)
- ✅ Código modular e bem organizado
- ✅ Testes unitários inclusos

## 🚀 Instalação Rápida

### ⚡ Verificação e Setup Automático (Recomendado)

Todos os scripts de setup foram unificados em `verificar_instalacao.py` que funciona em **Windows, Linux e macOS**.

**Apenas verificar dependências (sem instalar):**
```bash
python verificar_instalacao.py
```

**Instalar tudo automaticamente:**
```bash
# Método 1: Python direto (recomendado)
python verificar_instalacao.py --setup

# Método 2: Atalho no Windows
python setup.py

# Método 3: Atalho no Linux/macOS
bash setup.sh
```

**Ver ajuda completa:**
```bash
python verificar_instalacao.py --help
```

O script detecta automaticamente:
- ✓ Seu sistema operacional (Windows, Linux, macOS)
- ✓ Distribuição Linux (Ubuntu/Debian, Fedora/RHEL, Arch)
- ✓ Instala dependências do sistema necessárias
- ✓ Instala dependências Python via pip
- ✓ Verifica novamente se tudo foi instalado

### 📦 Instalação Manual

#### 1. Dependências do Sistema (Linux)

O PySide6 requer bibliotecas do sistema. Execute o comando apropriado:

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y libxcb-cursor0 libxcb-xinerama0 libxcb-xkb1 libxkbcommon-x11-0
```

**Fedora/RHEL:**
```bash
sudo dnf install -y libxcb xcb-util-cursor libxkbcommon-x11
```

**Arch Linux:**
```bash
sudo pacman -Syu --noconfirm libxcb xcb-util-cursor libxkbcommon-x11
```

**macOS:**
```bash
brew install qt@6
```

**Windows:**
Nenhuma dependência adicional necessária.

#### 2. Dependências Python

```bash
pip install -r requirements.txt
```

Ou manualmente:
```bash
pip install PySide6 matplotlib numpy pandas scipy openpyxl
```

#### 3. Ambiente Virtual (Opcional mas Recomendado)

```bash
# Criar ambiente
python -m venv .venv

# Ativar ambiente
# Linux/macOS:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate
```

## 📖 Como Usar

### Modo 1: Interface Gráfica (GUI) - Recomendado

```bash
python scalc.py
```

Ou explicitamente:
```bash
python scalc.py --gui
```

#### Passo a passo na interface:

1. **Carregar Arquivo**: Clique em "📁 Selecionar Arquivo Excel"
2. **Calcular Estatísticas**: Clique em "🔢 Calcular Estatísticas"
3. **Selecionar Variáveis**: Escolha as variáveis X e Y nos dropdowns
4. **Calcular Regressão**: Clique em "📈 Calcular Regressão Linear"
5. **Plotar Gráfico**: Clique em "🎨 Plotar Gráfico"

#### Recursos da interface:

- **Tab Gráfico**: Visualize o gráfico com barra de ferramentas (zoom, pan, salvar)
- **Tab Dados**: Veja os dados brutos do arquivo Excel
- **Tab Estatísticas**: Consulte estatísticas detalhadas de todas as variáveis

### Modo 2: Linha de Comando (CLI)

Para processamento direto sem interface:

```bash
python scalc.py --cli --arquivo dados.xlsx
```

Com parâmetros personalizados:

```bash
python scalc.py --cli \
    --arquivo dados.xlsx \
    --x-label "Tempo (s)" \
    --y-label "Distância (m)" \
    --titulo "Meu Gráfico"
```

#### Argumentos disponíveis:

- `--cli`: Ativa o modo linha de comando
- `--arquivo` ou `-f`: Caminho para o arquivo Excel (obrigatório no modo CLI)
- `--x-label`: Label do eixo X (padrão: "log(t) [s]")
- `--y-label`: Label do eixo Y (padrão: "log(d) [mm]")
- `--titulo`: Título do gráfico

Para ver todas as opções:
```bash
python scalc.py --help
```

## 📊 Formato dos Dados

### Estrutura esperada do arquivo Excel:

| x1   | x2   | x3   | xerr_instr | y1   | y2   | y3   | yerr_instr |
|------|------|------|------------|------|------|------|------------|
| 1.2  | 1.3  | 1.1  | 0.05       | 2.4  | 2.5  | 2.3  | 0.1        |
| 2.3  | 2.4  | 2.2  | 0.05       | 4.6  | 4.8  | 4.5  | 0.1        |

**Convenção de nomenclatura:**
- **Dados experimentais**: `x1`, `x2`, `x3`, `y1`, `y2`, `y3`, etc.
- **Erros instrumentais**: `xerr_instr`, `yerr_instr`, etc.

**Notas importantes:**
- Múltiplas medições da mesma variável devem ter o mesmo prefixo (ex: `x1`, `x2`, `x3`)
- O programa calcula automaticamente a média e os erros estatísticos
- Células vazias são ignoradas

## 📁 Estrutura do Projeto

```
scalc/
├── scalc.py                          # Arquivo principal
├── setup.py                          # Script de setup (Python)
├── setup.sh                          # Script de setup (Bash)
├── requirements.txt                  # Dependências Python
│
├── src/
│   ├── __init__.py
│   ├── core/                         # Lógica de negócio
│   │   ├── __init__.py
│   │   ├── statistics.py             # Cálculos estatísticos
│   │   └── regression.py             # Regressão linear
│   │
│   ├── visualization/                # Visualização e interface
│   │   ├── __init__.py
│   │   ├── gui.py                    # Interface gráfica (PySide6)
│   │   └── plots.py                  # Plotagem de gráficos
│   │
│   ├── data/                         # Dados e configuração
│   │   ├── __init__.py
│   │   └── config.py                 # Configurações globais
│   │
│   └── utils/                        # Utilidades gerais
│       └── __init__.py
│
├── tests/                            # Testes unitários
│   ├── __init__.py
│   ├── test_statistics.py            # Testes de estatística
│   └── test_regression.py            # Testes de regressão
│
├── docs/                             # Documentação
│   ├── GUIA_VISUAL.md                # Guia visual de uso
│   ├── PROJETO_COMPLETO.md           #
│   ├── API.md (futuro)               # Documentação de API
│   └── TROUBLESHOOTING.md (futuro)   # Solução de problemas
│
└── examples/                         # Exemplos de uso
    └── data/
        └── sample_data.xlsx
```

## 🎯 Funcionalidades

### Cálculos Estatísticos

- **Média**: Calculada a partir de múltiplas medições
- **Erro Estatístico**: Erro padrão da média com distribuição t de Student
- **Erro Instrumental**: Lido diretamente do arquivo
- **Erro Total**: Propagação quadrática dos erros

### Regressão Linear

- **Método dos Mínimos Quadrados**: Usando `scipy.stats.linregress`
- **Coeficiente de Determinação (R²)**: Mede a qualidade do ajuste (0 a 1)
- **Equação da reta**: y = mx + b

#### Interpretação de R²:

- **R² > 0.95**: Excelente ajuste
- **R² > 0.85**: Bom ajuste
- **R² > 0.70**: Ajuste moderado
- **R² < 0.70**: Ajuste fraco

### Visualização

- Gráfico de dispersão com barras de erro
- Reta de regressão linear
- Ferramentas interativas (zoom, pan, salvar)
- Exportação em diversos formatos

## 🧪 Executar Testes

```bash
# Executar todos os testes
python -m unittest discover tests/

# Executar teste específico
python -m unittest tests.test_statistics
python -m unittest tests.test_regression
```

## 📝 Uso Programático

```python
from src.core import Calcular_Estatisticas, RegLin
from src.visualization.plots import PlotarGrafico
import pandas as pd
import numpy as np

# Carregar dados
dados = pd.read_excel("dados.xlsx")

# Calcular estatísticas
medias, erros_est, erros_totais = Calcular_Estatisticas(dados)

# Preparar dados
x = np.array(medias['x'])
y = np.array(medias['y'])
x_err = np.array(erros_est['x'])
y_err = np.array(erros_est['y'])

# Calcular regressão
slope, intercept, r_squared = RegLin(x, y)

# Plotar
PlotarGrafico(
    set(zip(x, y)),
    x_err.tolist(),
    y_err.tolist(),
    str_x="X (unidade)",
    slope=slope,
    intercept=intercept,
    str_y="Y (unidade)",
    titulo="Regressão Linear"
)

print(f"Equação: y = {slope:.4f}x + {intercept:.4f}")
print(f"R² = {r_squared:.4f}")
```

## 🔧 Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'PySide6'"

```bash
pip install PySide6
```

### Erro: "qt.qpa.plugin: Could not load the Qt platform plugin"

Execute o script de setup:
```bash
bash setup.sh          # Linux/macOS
python setup.py        # Windows
```

### Gráfico não aparece (CLI)

Certifique-se de que o backend do matplotlib está configurado corretamente.

### Arquivo não encontrado

- Verifique o caminho do arquivo
- Use caminhos absolutos ou relativos corretos
- No Windows, use barras normais (`/`) ou duplas (`\\`)

## 📚 Documentação Adicional

No diretório docs/
- [GUIA_VISUAL.md](docs/GUIA_VISUAL.md) - Guia visual detalhado
- [PROJETO_COMPLETO.md](PROJETO_COMPLETO.md) - Especificações técnicas completas

## 🤝 Contribuindo

Sugestões e melhorias são bem-vindas! Sinta-se à vontade para:

1. Reportar bugs
2. Sugerir novas funcionalidades
3. Melhorar a documentação

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Autores

**Caio Aquilino Merino**
- GitHub: [@ZilchHarpy](https://github.com/ZilchHarpy)
- Email: caioaquilinomerino@gmail.com

## 📞 Suporte

Se encontrar algum problema, abra uma [issue](https://github.com/ZilchHarpy/SCalc/issues) no GitHub.

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no repositório!
