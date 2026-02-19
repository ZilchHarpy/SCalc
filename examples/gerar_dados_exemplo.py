"""
Script para gerar um arquivo Excel de exemplo compativel com o SCalc.

Formato gerado:
  - Coluna 'Dados': identificadores no formato <prefixo>_<n>
  - Coluna 'I_err': erro instrumental de cada ponto
  - Colunas '1', '2', '3': repeticoes da medicao

Relacao simulada: b ≈ 2a + 3  (com ruido gaussiano)
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

# Garantir que o script funciona tanto rodado diretamente quanto
# a partir da raiz do projeto
RAIZ = Path(__file__).parent.parent
SAIDA = RAIZ / 'src' / 'data' / 'test_table.xlsx'

np.random.seed(42)

N_PONTOS    = 8    # numero de pontos por variavel (a_1 ... a_8, b_1 ... b_8)
N_REPS      = 3    # numero de repeticoes por ponto
I_ERR_A     = 0.05
I_ERR_B     = 0.10
RUIDO_A     = 0.08
RUIDO_B     = 0.25

# Valores "verdadeiros" de a (eixo X)
a_true = np.linspace(1.0, 8.0, N_PONTOS)

# Valores "verdadeiros" de b (eixo Y), com relacao b = 2a + 3
b_true = 2.0 * a_true + 3.0

# Gerar repeticoes com ruido
a_reps = [a_true + np.random.normal(0, RUIDO_A, N_PONTOS) for _ in range(N_REPS)]
b_reps = [b_true + np.random.normal(0, RUIDO_B, N_PONTOS) for _ in range(N_REPS)]

# Montar identificadores: a_1, a_2, ..., a_N, b_1, b_2, ..., b_N
ids_a = [f'a_{i+1}' for i in range(N_PONTOS)]
ids_b = [f'b_{i+1}' for i in range(N_PONTOS)]
identificadores = ids_a + ids_b

# Erros instrumentais por linha
erros = [I_ERR_A] * N_PONTOS + [I_ERR_B] * N_PONTOS

# Colunas de repeticao
rep_cols = {}
for r in range(N_REPS):
    valores_a = list(a_reps[r])
    valores_b = list(b_reps[r])
    rep_cols[str(r + 1)] = valores_a + valores_b

# Montar DataFrame
df = pd.DataFrame({'Dados': identificadores, 'I_err': erros, **rep_cols})

# Salvar
SAIDA.parent.mkdir(parents=True, exist_ok=True)
df.to_excel(SAIDA, index=False)

print(f"Arquivo gerado: {SAIDA}")
print(f"  Variaveis : a ({N_PONTOS} pontos), b ({N_PONTOS} pontos)")
print(f"  Repeticoes: {N_REPS} por ponto")
print(f"  Relacao   : b = 2a + 3  (com ruido)")
print()
print(df.to_string(index=False))
