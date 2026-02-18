"""
Testes para o modulo de regressao linear (regression.py).

RegLin(x, y) -> (slope, intercept, r_squared)
    slope      : coeficiente angular (float)
    intercept  : coeficiente linear  (float)
    r_squared  : coeficiente de determinacao R^2 (float, 0 a 1)
"""

import unittest
import math
import numpy as np
from src.core import RegLin


class TestRegLin(unittest.TestCase):
    """Testes para a funcao RegLin()."""

    # ------------------------------------------------------------------ #
    #  Tipos de retorno                                                    #
    # ------------------------------------------------------------------ #

    def test_retorna_tres_floats(self):
        """RegLin deve retornar uma tupla de tres floats."""
        resultado = RegLin([1.0, 2.0, 3.0], [2.0, 4.0, 6.0])
        self.assertIsInstance(resultado, tuple)
        self.assertEqual(len(resultado), 3)
        slope, intercept, r_squared = resultado
        self.assertIsInstance(slope,     float)
        self.assertIsInstance(intercept, float)
        self.assertIsInstance(r_squared, float)

    # ------------------------------------------------------------------ #
    #  Reta perfeita: y = 2x                                              #
    # ------------------------------------------------------------------ #

    def test_reta_perfeita_slope(self):
        """Para y = 2x, slope deve ser exatamente 2.0."""
        slope, _, _ = RegLin([1.0, 2.0, 3.0, 4.0, 5.0],
                              [2.0, 4.0, 6.0, 8.0, 10.0])
        self.assertAlmostEqual(slope, 2.0, places=10)

    def test_reta_perfeita_intercept(self):
        """Para y = 2x, intercept deve ser exatamente 0.0."""
        _, intercept, _ = RegLin([1.0, 2.0, 3.0, 4.0, 5.0],
                                  [2.0, 4.0, 6.0, 8.0, 10.0])
        self.assertAlmostEqual(intercept, 0.0, places=10)

    def test_reta_perfeita_r2(self):
        """Para y = 2x perfeito, R^2 deve ser 1.0."""
        _, _, r_squared = RegLin([1.0, 2.0, 3.0, 4.0, 5.0],
                                  [2.0, 4.0, 6.0, 8.0, 10.0])
        self.assertAlmostEqual(r_squared, 1.0, places=10)

    # ------------------------------------------------------------------ #
    #  Reta com intercepto nao nulo: y = 3x + 1                           #
    # ------------------------------------------------------------------ #

    def test_reta_com_intercepto(self):
        """Para y = 3x + 1, slope ≈ 3 e intercept ≈ 1."""
        x = [0.0, 1.0, 2.0, 3.0, 4.0]
        y = [1.0, 4.0, 7.0, 10.0, 13.0]
        slope, intercept, r_squared = RegLin(x, y)
        self.assertAlmostEqual(slope,     3.0, places=10)
        self.assertAlmostEqual(intercept, 1.0, places=10)
        self.assertAlmostEqual(r_squared, 1.0, places=10)

    # ------------------------------------------------------------------ #
    #  Dados com ruido                                                     #
    # ------------------------------------------------------------------ #

    def test_dados_com_ruido_slope_aproximado(self):
        """Com ruido gaussiano pequeno, slope deve ser proximo ao valor real."""
        np.random.seed(42)
        x = np.linspace(1.0, 5.0, 10)
        y = 2.0 * x + 0.5 + np.random.normal(0, 0.1, 10)
        slope, intercept, r_squared = RegLin(x.tolist(), y.tolist())
        self.assertAlmostEqual(slope,     2.0, delta=0.2)
        self.assertAlmostEqual(intercept, 0.5, delta=0.3)

    def test_dados_com_ruido_r2_alto(self):
        """Com ruido pequeno, R^2 deve ser maior que 0.99."""
        np.random.seed(42)
        x = np.linspace(1.0, 5.0, 10)
        y = 2.0 * x + 0.5 + np.random.normal(0, 0.1, 10)
        _, _, r_squared = RegLin(x.tolist(), y.tolist())
        self.assertGreater(r_squared, 0.99)

    # ------------------------------------------------------------------ #
    #  Caso minimo: dois pontos                                            #
    # ------------------------------------------------------------------ #

    def test_dois_pontos_determinam_reta_perfeita(self):
        """
        Dois pontos sempre determinam uma reta exata (R^2 = 1.0).
        Para (1, 2) e (3, 8): slope = 3, intercept = -1.
        """
        slope, intercept, r_squared = RegLin([1.0, 3.0], [2.0, 8.0])
        self.assertAlmostEqual(slope,     3.0, places=10)
        self.assertAlmostEqual(intercept, -1.0, places=10)
        self.assertAlmostEqual(r_squared, 1.0,  places=10)

    # ------------------------------------------------------------------ #
    #  Aceita numpy arrays alem de listas Python                          #
    # ------------------------------------------------------------------ #

    def test_aceita_numpy_array(self):
        """RegLin deve funcionar com numpy arrays como entrada."""
        x = np.array([1.0, 2.0, 3.0])
        y = np.array([2.0, 4.0, 6.0])
        slope, intercept, r_squared = RegLin(x, y)
        self.assertAlmostEqual(slope, 2.0, places=10)

    # ------------------------------------------------------------------ #
    #  R^2 dentro do intervalo [0, 1]                                     #
    # ------------------------------------------------------------------ #

    def test_r2_no_intervalo_valido(self):
        """R^2 deve estar sempre no intervalo [0, 1]."""
        np.random.seed(0)
        x = np.random.uniform(0, 10, 20).tolist()
        y = np.random.uniform(0, 10, 20).tolist()   # dados sem correlacao
        _, _, r_squared = RegLin(x, y)
        self.assertGreaterEqual(r_squared, 0.0)
        self.assertLessEqual(r_squared,    1.0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
