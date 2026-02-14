"""
Testes para o modulo de Estatistica
"""

import unittest
import pandas as pd
import numpy as np
from src.core import Calcular_Estatisticas, Particionar


class TestStatistics(unittest.TestCase):
    """Testes para funcoes de estatistica"""
    
    def setUp(self):
        """Configura dados de teste"""
        # Criar um DataFrame de exemplo
        self.df = pd.DataFrame({
            'x1': [1.0, 2.0, 3.0],
            'x2': [1.1, 2.1, 3.1],
            'x3': [0.9, 1.9, 2.9],
            'xerr_instr': [0.1, 0.1, 0.1],
            'y1': [2.0, 4.0, 6.0],
            'y2': [2.1, 4.1, 6.1],
            'y3': [1.9, 3.9, 5.9],
            'yerr_instr': [0.2, 0.2, 0.2],
        })
    
    def test_particionar(self):
        """Testa a funcao Particionar"""
        dados_brutos, erros = Particionar(self.df)
        
        # Verificar se as chaves esperadas estao presentes
        self.assertIn('x1', dados_brutos)
        self.assertIn('y1', dados_brutos)
        self.assertIn('xerr_instr', erros)
        self.assertIn('yerr_instr', erros)
    
    def test_calcular_estatisticas(self):
        """Testa a funcao Calcular_Estatisticas"""
        medias, erros_est, erros_totais = Calcular_Estatisticas(self.df)
        
        # Verificar se as variaveis foram calculadas
        self.assertIn('x', medias)
        self.assertIn('y', medias)
        
        # Verificar comprimento das listas
        self.assertEqual(len(medias['x']), 3)
        self.assertEqual(len(medias['y']), 3)


if __name__ == '__main__':
    unittest.main()
