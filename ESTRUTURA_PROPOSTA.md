# Estrutura Proposta para Organização do SCalc

## Estrutura Atual
```
scalc/
├── scalc.py
├── setup.py
├── setup.sh
├── requirements.txt
├── README.md
├── src/
│   ├── __init__.py
│   ├── utils.py
│   ├── visualisation.py
│   └── data/
├── testes/
│   ├── __init__.py
│   ├── main_testes.py
│   └── utils_testes.py
└── examples/
```

## Estrutura Recomendada (Mais Profissional)
```
scalc/
├── scalc.py                          # Arquivo principal (entry point)
├── setup.py
├── setup.sh
├── requirements.txt
├── README.md
│
├── src/                              # Código principal
│   ├── __init__.py
│   │
│   ├── core/                         # Lógica de negócio
│   │   ├── __init__.py
│   │   ├── statistics.py             # Calcular_Estatisticas (antes: utils.py)
│   │   ├── regression.py             # RegLin (antes: utils.py)
│   │   └── data_processing.py        # Particionar (antes: utils.py)
│   │
│   ├── visualization/                # Interface e gráficos
│   │   ├── __init__.py
│   │   ├── gui.py                    # Interface gráfica (antes: visualisation.py)
│   │   └── plots.py                  # PlotarGrafico (antes: utils.py)
│   │
│   ├── data/                         # Dados e configurações
│   │   ├── __init__.py
│   │   └── config.py                 # Configurações (NOVO)
│   │
│   └── utils/                        # Utilitários gerais (NOVO)
│       ├── __init__.py
│       └── helpers.py                # Funções auxiliares genéricas
│
├── tests/                            # Testes (antes: testes/)
│   ├── __init__.py
│   ├── test_statistics.py            # Testes de estatística
│   ├── test_regression.py            # Testes de regressão
│   └── test_gui.py                   # Testes de interface
│
├── examples/                         # Exemplos de uso
│   ├── basic_example.py
│   └── data/
│       └── sample_data.xlsx
│
└── docs/                             # Documentação (NOVO)
    ├── GUIA_VISUAL.md                (mover daqui)
    ├── API.md                        # Documentação de API
    └── TROUBLESHOOTING.md            # Solução de problemas
```

## Como Fazer a Migração sem Quebrar Nada

### Passo 1: Criar nova estrutura
```bash
mkdir -p src/core
mkdir -p src/visualization
mkdir -p src/utils
mkdir -p docs
mv GUIA_VISUAL.md docs/
```

### Passo 2: Separar as funções em novos arquivos

**src/core/statistics.py** (com Calcular_Estatisticas, Particionar)
**src/core/regression.py** (com RegLin)
**src/visualization/plots.py** (com PlotarGrafico)
**src/visualization/gui.py** (com visualisation.py renomeado)

### Passo 3: Atualizar imports
Use imports relativos consistentes:

```python
# Em scalc.py (arquivo principal)
from src.core.statistics import Calcular_Estatisticas
from src.core.regression import RegLin
from src.visualization.plots import PlotarGrafico

# Em src/visualization/gui.py
from src.core.statistics import Calcular_Estatisticas
from src.core.regression import RegLin

# Em src/core/statistics.py (uso interno)
from src.utils.helpers import parse_data
```

### Passo 4: Usar __init__.py para facilitar imports

**src/__init__.py**
```python
from src.core import Calcular_Estatisticas, RegLin, Particionar
from src.visualization import PlotarGrafico
```

Isso permite fazer:
```python
from src import Calcular_Estatisticas, RegLin
```

### Passo 5: Criar arquivo de configuração

**src/data/config.py**
```python
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
EXAMPLES_DIR = os.path.join(BASE_DIR, 'examples')
```

Depois use em qualquer arquivo:
```python
from src.data.config import DATA_DIR

file_path = os.path.join(DATA_DIR, 'seu_arquivo.xlsx')
```

## Benefícios desta Reorganização

✅ **Modularidade**: Cada módulo tem uma responsabilidade clara
✅ **Manutenibilidade**: Fácil encontrar e modificar código
✅ **Escalabilidade**: Adicionar novos módulos sem quebrar existentes
✅ **Testabilidade**: Mais fácil escrever testes unitários
✅ **Profissionalismo**: Segue padrões da indústria (PEP 20)
✅ **Compatibilidade**: Todos os imports funcionam perfeitamente

## Resumo do Impacto nos Arquivos

| Arquivo | Mudança |
|---------|---------|
| scalc.py | Atualizar imports |
| src/visualisation.py → src/visualization/gui.py | Renomear + atualizar imports |
| src/utils.py → src/core/ | Separar em 3 arquivos |
| testes/ → tests/ | Renomear + atualizar imports |

**IMPORTANTE**: Nenhum código interno muda, apenas a organização e imports!
