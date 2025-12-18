"""
Testes para o módulo de Regressão Linear
"""

import unittest
import numpy as np
from src.core import RegLin


class TestRegression(unittest.TestCase):
    """Testes para funções de regressão linear"""
    
    def setUp(self):
        """Configura dados de teste"""
        # Dados lineares simples
        self.x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        self.y = np.array([2.0, 4.0, 6.0, 8.0, 10.0])  # y = 2x
    
    def test_reglin(self):
        """Testa a função RegLin"""
        slope, intercept, r_squared = RegLin(self.x, self.y)
        
        # Verificar se os valores são razoáveis
        self.assertAlmostEqual(slope, 2.0, places=1)  # Esperado: 2.0
        self.assertAlmostEqual(intercept, 0.0, places=1)  # Esperado: 0.0
        self.assertGreater(r_squared, 0.99)  # R² deve ser próximo a 1.0
    
    def test_reglin_com_erro(self):
        """Testa RegLin com dados com erro"""
        # Dados com pequeno erro aleatório
        np.random.seed(42)
        x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        y = 2.0 * x + 0.5 + np.random.normal(0, 0.2, 5)
        
        slope, intercept, r_squared = RegLin(x, y)
        
        # Verificar se os valores são próximos aos esperados
        self.assertGreater(slope, 1.8)
        self.assertLess(slope, 2.2)
        self.assertGreater(r_squared, 0.95)


if __name__ == '__main__':
    unittest.main()
