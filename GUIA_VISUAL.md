# 🎨 Guia Visual da Interface - SCalc

## Layout da Interface

A interface está dividida em **duas áreas principais**:

### 📌 Painel Esquerdo - Controles (1/3 da tela)

```
┌─────────────────────────────────────┐
│  📊 SCalc - Análise de Regressão   │
├─────────────────────────────────────┤
│                                     │
│  1. CARREGAR ARQUIVO                │
│  ┌───────────────────────────────┐ │
│  │ Nenhum arquivo carregado      │ │
│  │ [📁 Selecionar Arquivo Excel] │ │
│  └───────────────────────────────┘ │
│                                     │
│  2. CONFIGURAR EIXOS                │
│  ┌───────────────────────────────┐ │
│  │ Eixo X: [log(t) [s]        ] │ │
│  │ Eixo Y: [log(d) [mm]       ] │ │
│  │ Título: [Gráfico...        ] │ │
│  └───────────────────────────────┘ │
│                                     │
│  3. SELECIONAR VARIÁVEIS            │
│  ┌───────────────────────────────┐ │
│  │ Var X: [▼ Selecione       ] │ │
│  │ Var Y: [▼ Selecione       ] │ │
│  └───────────────────────────────┘ │
│                                     │
│  4. AÇÕES                           │
│  ┌───────────────────────────────┐ │
│  │ [🔢 Calcular Estatísticas  ] │ │
│  │ [📈 Calcular Regressão     ] │ │
│  │ [🎨 Plotar Gráfico         ] │ │
│  │ [🗑️ Limpar Tudo            ] │ │
│  └───────────────────────────────┘ │
│                                     │
│  📋 RESULTADOS                      │
│  ┌───────────────────────────────┐ │
│  │ Equação: y = 2.15x + 0.02   │ │
│  │ R² = 0.9876                  │ │
│  │ ...                           │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
```

### 📊 Painel Direito - Visualização (2/3 da tela)

```
┌─────────────────────────────────────────────────────────────┐
│  [📊 Gráfico] [📄 Dados] [📈 Estatísticas]                  │
├─────────────────────────────────────────────────────────────┤
│  🔍 🏠 ◀ ▶ 💾  (Barra de ferramentas do matplotlib)        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│              GRÁFICO DE DISPERSÃO                           │
│                                                             │
│    y │                                                      │
│      │         ● (ponto com barras de erro)                │
│      │       ● ╱                                            │
│      │     ●  ╱  (linha de regressão)                      │
│      │   ●   ╱                                              │
│      │ ●    ╱                                               │
│      │     ╱                                                │
│      │    ╱                                                 │
│      │   ╱  ● Dados experimentais                          │
│      │  ╱   ─ y = 2.15x + 0.02                             │
│      │ ╱      R² = 0.9876                                  │
│      └─────────────────────────────────────► x             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Fluxo de Trabalho

### Passo 1: Carregar Arquivo
- Clique em "📁 Selecionar Arquivo Excel"
- Navegue até seu arquivo .xlsx
- O sistema carrega e mostra na tab "📄 Dados"

### Passo 2: Calcular Estatísticas
- Clique em "🔢 Calcular Estatísticas"
- Sistema calcula médias e erros
- Variáveis aparecem nos dropdowns

### Passo 3: Selecionar Variáveis
- Escolha variável X (independente)
- Escolha variável Y (dependente)

### Passo 4: Calcular Regressão
- Clique em "📈 Calcular Regressão Linear"
- Resultados aparecem no painel de resultados

### Passo 5: Visualizar
- Clique em "🎨 Plotar Gráfico"
- Gráfico aparece com pontos e reta

## 🛠️ Ferramentas Interativas

### Barra de Ferramentas do Matplotlib:
- 🏠 **Home**: Volta ao zoom original
- ◀ **Back**: Volta para visualização anterior
- ▶ **Forward**: Avança para visualização seguinte
- 🔍 **Zoom**: Arrastar para fazer zoom em região
- ✋ **Pan**: Arrastar para mover o gráfico
- 💾 **Save**: Salvar gráfico (PNG, PDF, SVG, etc)

## 📑 Tabs de Visualização

### Tab 1: 📊 Gráfico
- Gráfico de dispersão com barras de erro
- Reta de regressão linear
- Legenda com equação e R²
- Ferramentas interativas

### Tab 2: 📄 Dados
- Tabela com dados do Excel
- Visualização de todas as colunas
- Scroll horizontal e vertical

### Tab 3: 📈 Estatísticas
- Médias calculadas para cada variável
- Erros estatísticos
- Erros instrumentais
- Formato texto detalhado

## 🎨 Cores e Estilo

- **Pontos experimentais**: 🔴 Vermelho (círculos)
- **Barras de erro**: 🟥 Vermelho escuro
- **Linha de regressão**: 🔵 Azul (linha sólida)
- **Grade**: Cinza claro pontilhada
- **Fundo**: Branco

## ⌨️ Atalhos Rápidos (futuro)

- `Ctrl+O`: Abrir arquivo
- `Ctrl+S`: Salvar gráfico
- `Ctrl+R`: Calcular regressão
- `F5`: Atualizar gráfico
- `Ctrl+Q`: Sair

## 📱 Responsividade

A interface se adapta ao tamanho da janela:
- Mínimo: 1000x600 pixels
- Recomendado: 1400x900 pixels
- Máximo: Sem limite

O splitter permite redimensionar os painéis arrastando a divisória.

## 🎯 Exemplo Prático

1. Abra o programa: `python scalc.py`
2. Clique em "📁 Selecionar Arquivo Excel"
3. Selecione `src/data/TBTeste.xlsx`
4. Clique em "🔢 Calcular Estatísticas"
5. Verifique que "x" e "y" apareceram nos dropdowns
6. Clique em "📈 Calcular Regressão Linear"
7. Leia os resultados: `y = 2.000x + 3.000` (aproximadamente)
8. Clique em "🎨 Plotar Gráfico"
9. Use as ferramentas para explorar o gráfico
10. Salve o gráfico usando o botão 💾

---

**Pronto para usar! 🚀**
