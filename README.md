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

## 🚀 Instalação

### Requisitos

- Python 3.8 ou superior

### 1. Instalar dependências do sistema (Linux)

O PySide6 requer bibliotecas do sistema para funcionar. Execute o comando apropriado para sua distribuição:

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y libxcb-cursor0 libxcb-xinerama0 libxcb-xkb1 libxkbcommon-x11-0
```

**Fedora/RHEL:**
```bash
sudo dnf install libxcb xcb-util-cursor libxkbcommon-x11
```

**Arch Linux:**
```bash
sudo pacman -S libxcb xcb-util-cursor libxkbcommon-x11
```

**macOS:**
```bash
brew install qt@6
```

**Windows:**
Nenhuma dependência adicional é necessária.

### 2. Instalar dependências Python

```bash
pip install -r requirements.txt
```

Ou manualmente:

```bash
pip install PySide6 matplotlib numpy pandas scipy openpyxl
```

### ⚡ Instalação Rápida (Automática)

Para instalar todas as dependências automaticamente, use um dos scripts fornecidos:

**Linux/macOS:**
```bash
bash setup.sh
```

**Windows (PowerShell):**
```powershell
python setup.py
```

**Qualquer plataforma (usando Python):**
```bash
python setup.py
```

## 📖 Como Usar

### Modo 1: Interface Gráfica (GUI) - Recomendado

Execute o programa sem argumentos para abrir a interface gráfica:

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
python scalc.py --cli --arquivo src/data/TBTeste.xlsx
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

## 📢 Dicas e recomendações

**As recomendações a seguir foram baseadas visando possíveis imprevistos**

### Arquivo `PROJETO_COMPLETO.md`

Neste arquivo reside detalhes da estrutura do projeto e comandos de auxílio com várias especificações que não foram tratadas neste

### Criação de um ambiente python

Criando o ambiente:

```bash
python -m venv .venv
```

Ativando o ambiente:

- Windows:
```bash
venv\Scripts\activate
```
- Linux/macOS:
```bash
source venv/bin/activate
```

### Ajuda

Para ver todas as opções disponíveis:

```bash
python scalc.py --help
```

## 📊 Formato dos Dados

### Estrutura esperada do arquivo Excel:

O arquivo deve conter colunas com a seguinte nomenclatura:

- **Dados experimentais**: `x1`, `x2`, `x3`, `y1`, `y2`, `y3`, etc.
- **Erros instrumentais**: `xerr_instr`, `yerr_instr`, etc.

Exemplo:

| x1   | x2   | x3   | xerr_instr | y1   | y2   | y3   | yerr_instr |
|------|------|------|------------|------|------|------|------------|
| 1.2  | 1.3  | 1.1  | 0.05       | 2.4  | 2.5  | 2.3  | 0.1        |
| 2.3  | 2.4  | 2.2  | 0.05       | 4.6  | 4.8  | 4.5  | 0.1        |
| ...  | ...  | ...  | ...        | ...  | ...  | ...  | ...        |

**Notas importantes:**
- Múltiplas medições da mesma variável devem ter o mesmo prefixo (ex: `x1`, `x2`, `x3`)
- O programa calcula automaticamente a média e os erros estatísticos
- Células vazias são ignoradas

## 🎯 Funcionalidades

### Cálculos Estatísticos

- **Média**: Calculada a partir de múltiplas medições
- **Erro Estatístico**: Erro padrão da média
- **Erro Instrumental**: Lido diretamente do arquivo
- **Erro Total**: Propagação quadrática dos erros

### Regressão Linear

- **Método dos Mínimos Quadrados**: Usando `scipy.stats.linregress`
- **Coeficiente de Determinação (R²)**: Mede a qualidade do ajuste
- **Equação da reta**: y = mx + b

### Visualização

- Gráfico de dispersão com barras de erro
- Reta de regressão linear
- Ferramentas interativas (zoom, pan, salvar)
- Exportação em diversos formatos (PNG, PDF, SVG, EPS)

## 📁 Estrutura central do Projeto

```
scalc/
├── scalc.py                 # Arquivo principal
├── src/
│   ├── utils.py            # Funções utilitárias
│   ├── visualisation.py    # Interface gráfica
│   └── data/
│       └── TBTeste.xlsx    # Arquivo de exemplo
├── GUIA_VISUAL.md          # Arquivo guia na utilização do software
├── PROJETO_COMPLETO        # Arquivo mais detalhado sobre a estrutura do projeto
└── README.md               # Este arquivo
```

## 🔧 Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'PySide6'"

```bash
pip install PySide6
```

### Erro: "No module named 'openpyxl'"

```bash
pip install openpyxl
```

### Gráfico não aparece

- **Modo CLI**: Certifique-se de que o backend do matplotlib está configurado corretamente
- **Modo GUI**: Verifique se há erros no console

### Arquivo não encontrado

- Verifique o caminho do arquivo
- Use caminhos absolutos ou relativos corretos
- No Windows, use barras invertidas duplas (`\\`) ou barras normais (`/`)

## 📝 Exemplo de Uso Completo

```python
# Importar módulos
from src.utils import Calcular_Estatisticas, RegLin, PlotarGrafico
import pandas as pd
import numpy as np

# Carregar dados
dados = pd.read_excel("src/data/TBTeste.xlsx")

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
    str_x="X",
    str_y="Y",
    slope=slope,
    intercept=intercept,
    titulo="Regressão Linear"
)

print(f"Equação: y = {slope:.4f}x + {intercept:.4f}")
print(f"R² = {r_squared:.4f}")
```

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

Se encontrar algum problema ou tiver sugestões, abra uma [issue](https://github.com/ZilchHarpy/SCalc/issues) no GitHub.

---
## 🤖 IA

Neste projeto foram usadas ferramentas de inteligência artificial para auxílio de escrita dos arquivos 'markdown e o arquivo de dependências  'requirements.txt'

⭐ Se este projeto foi útil para você, considere dar uma estrela no repositório!
