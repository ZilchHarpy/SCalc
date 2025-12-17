"""
Script para gerar um arquivo Excel de exemplo para o SCalc
Este arquivo cria dados simulados seguindo o formato esperado
"""

import pandas as pd
import numpy as np

# Definir seed para reprodutibilidade
np.random.seed(42)

# Criar dados simulados
# Relação: y ≈ 2x + 3 + ruído
n_pontos = 10

# Gerar 3 medições de X
x1 = np.linspace(1, 10, n_pontos) + np.random.normal(0, 0.1, n_pontos)
x2 = np.linspace(1, 10, n_pontos) + np.random.normal(0, 0.1, n_pontos)
x3 = np.linspace(1, 10, n_pontos) + np.random.normal(0, 0.1, n_pontos)

# Erro instrumental de X
xerr_instr = [0.05] * n_pontos

# Gerar 3 medições de Y (com relação linear y = 2x + 3)
y1 = 2 * x1 + 3 + np.random.normal(0, 0.3, n_pontos)
y2 = 2 * x2 + 3 + np.random.normal(0, 0.3, n_pontos)
y3 = 2 * x3 + 3 + np.random.normal(0, 0.3, n_pontos)

# Erro instrumental de Y
yerr_instr = [0.1] * n_pontos

# Criar DataFrame
dados = pd.DataFrame({
    'x1': x1,
    'x2': x2,
    'x3': x3,
    'xerr_instr': xerr_instr,
    'y1': y1,
    'y2': y2,
    'y3': y3,
    'yerr_instr': yerr_instr
})

# Salvar em Excel
caminho_saida = 'src/data/TBTeste.xlsx'
dados.to_excel(caminho_saida, index=False)

print(f"✓ Arquivo criado com sucesso: {caminho_saida}")
print(f"  Pontos: {n_pontos}")
print(f"  Relação real: y = 2x + 3")
print("\nPrimeiras linhas:")
print(dados.head())
print("\nEstatísticas:")
print(f"  X médio: {dados[['x1', 'x2', 'x3']].mean().mean():.2f}")
print(f"  Y médio: {dados[['y1', 'y2', 'y3']].mean().mean():.2f}")
