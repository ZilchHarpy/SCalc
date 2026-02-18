"""
Testes para o modulo de estatistica (statistics.py).

Estrutura esperada pelo particionar():
    - Coluna cujo nome contenha "dados" (case-insensitive): identificadores no
      formato <prefixo>_<n>, ex: a_1, a_2, b_1.
    - Colunas numericas (qualquer nome sem "dados" e sem indicador de erro):
      cada coluna e uma repeticao da medicao.
    - Coluna de erro instrumental: nome deve conter simultaneamente um indicador
      de erro ("err"/"error"/"erro") E um indicador de instrumental
      ("i"/"instr"/"instrumental"). Ex: I_err, xerr_instr.

calcular_estatisticas() retorna um pd.DataFrame com colunas:
    ['Dados', 'Media', 'S_err', 'T_err']
"""

import math
import unittest

import pandas as pd

from src.core import calcular_estatisticas, particionar
from src.core.exceptions import DadosInvalidosException


def _df_padrao():
    """
    DataFrame no formato correto para o SCalc.

    Grupos:
        a -> pontos a_1, a_2, a_3  (3 repeticoes cada, erro instrumental 0.10)
        b -> pontos b_1, b_2, b_3  (3 repeticoes cada, erro instrumental 0.20)

    Medias esperadas:
        a_1 = mean(1.0, 1.1, 0.9) = 1.0
        a_2 = mean(2.0, 2.1, 1.9) = 2.0
        a_3 = mean(3.0, 3.1, 2.9) = 3.0
        b_1 = mean(2.0, 2.1, 1.9) = 2.0
        b_2 = mean(4.0, 4.1, 3.9) = 4.0
        b_3 = mean(6.0, 6.1, 5.9) = 6.0
    """
    return pd.DataFrame({
        'Dados': ['a_1', 'a_2', 'a_3', 'b_1', 'b_2', 'b_3'],
        'I_err': [0.10,  0.10,  0.10,  0.20,  0.20,  0.20],
        '1':     [1.0,   2.0,   3.0,   2.0,   4.0,   6.0],
        '2':     [1.1,   2.1,   3.1,   2.1,   4.1,   6.1],
        '3':     [0.9,   1.9,   2.9,   1.9,   3.9,   5.9],
    })


def _df_repeticao_unica():
    """DataFrame com apenas uma repeticao por ponto (S_err deve ser 0)."""
    return pd.DataFrame({
        'Dados': ['a_1', 'a_2', 'b_1', 'b_2'],
        'I_err': [0.05,  0.05,  0.10,  0.10],
        '1':     [1.0,   2.0,   2.0,   4.0],
    })


# --------------------------------------------------------------------------- #
#  TestParticionar                                                              #
# --------------------------------------------------------------------------- #

class TestParticionar(unittest.TestCase):
    """Testes para a funcao particionar()."""

    def test_retorna_tres_valores(self):
        """particionar deve retornar exatamente (dados_brutos, erros_instr, dados_keys)."""
        resultado = particionar(_df_padrao())
        self.assertIsInstance(resultado, tuple)
        self.assertEqual(len(resultado), 3)

    def test_prefixos_extraidos(self):
        """Grupos 'a' e 'b' devem ser chaves de dados_brutos."""
        dados_brutos, _, _ = particionar(_df_padrao())
        self.assertIn('a', dados_brutos)
        self.assertIn('b', dados_brutos)

    def test_chaves_internas(self):
        """Cada grupo deve conter as chaves a_1, a_2, a_3 (ou b_*)."""
        dados_brutos, _, _ = particionar(_df_padrao())
        self.assertSetEqual(set(dados_brutos['a'].keys()), {'a_1', 'a_2', 'a_3'})
        self.assertSetEqual(set(dados_brutos['b'].keys()), {'b_1', 'b_2', 'b_3'})

    def test_valores_corretos(self):
        """Os valores de cada chave devem ser as repeticoes da linha correspondente."""
        dados_brutos, _, _ = particionar(_df_padrao())
        # a_1 deve conter as tres repeticoes da primeira linha do grupo a
        self.assertAlmostEqual(sum(dados_brutos['a']['a_1']) / 3, 1.0, places=5)

    def test_erros_instrumentais_extraidos(self):
        """erros_instr deve ter chaves para os prefixos 'a' e 'b'."""
        _, erros_instr, _ = particionar(_df_padrao())
        self.assertIn('a', erros_instr)
        self.assertIn('b', erros_instr)

    def test_erros_instrumentais_valores(self):
        """Erros instrumentais devem coincidir com a coluna I_err."""
        _, erros_instr, _ = particionar(_df_padrao())
        self.assertAlmostEqual(erros_instr['a']['a_1'], 0.10, places=5)
        self.assertAlmostEqual(erros_instr['b']['b_1'], 0.20, places=5)

    def test_dados_keys_contagem(self):
        """dados_keys deve registrar quantos pontos ha em cada grupo."""
        _, _, dados_keys = particionar(_df_padrao())
        self.assertEqual(dados_keys['a'], 3)
        self.assertEqual(dados_keys['b'], 3)

    def test_dataframe_vazio_levanta_excecao(self):
        """DataFrame vazio deve levantar DadosInvalidosException."""
        with self.assertRaises(DadosInvalidosException):
            particionar(pd.DataFrame())

    def test_nan_em_repeticoes_ignorado(self):
        """Celulas NaN em colunas de repeticao devem ser ignoradas sem erro."""
        df = pd.DataFrame({
            'Dados': ['a_1', 'a_2', 'b_1', 'b_2'],
            'I_err': [0.05,  0.05,  0.10,  0.10],
            '1':     [1.0,   2.0,   2.0,   4.0],
            '2':     [1.1,   None,  2.1,   None],
        })
        # Nao deve lancar excecao
        dados_brutos, _, _ = particionar(df)
        self.assertIn('a', dados_brutos)


# --------------------------------------------------------------------------- #
#  TestCalcularEstatisticas                                                    #
# --------------------------------------------------------------------------- #

class TestCalcularEstatisticas(unittest.TestCase):
    """Testes para a funcao calcular_estatisticas()."""

    def test_retorna_dataframe(self):
        """calcular_estatisticas deve retornar um pd.DataFrame."""
        resultado = calcular_estatisticas(_df_padrao())
        self.assertIsInstance(resultado, pd.DataFrame)

    def test_colunas_presentes(self):
        """DataFrame de saida deve ter as colunas ['Dados', 'Media', 'S_err', 'T_err']."""
        resultado = calcular_estatisticas(_df_padrao())
        for coluna in ('Dados', 'Media', 'S_err', 'T_err'):
            self.assertIn(coluna, resultado.columns)

    def test_numero_de_linhas(self):
        """Deve haver uma linha por identificador (6 no total: 3 de 'a' + 3 de 'b')."""
        resultado = calcular_estatisticas(_df_padrao())
        self.assertEqual(len(resultado), 6)

    def test_medias_corretas(self):
        """Media de a_1 deve ser 1.0, de a_2 deve ser 2.0, de a_3 deve ser 3.0."""
        resultado = calcular_estatisticas(_df_padrao())
        resultado = resultado.set_index('Dados')

        self.assertAlmostEqual(resultado.loc['a_1', 'Media'], 1.0, places=5)
        self.assertAlmostEqual(resultado.loc['a_2', 'Media'], 2.0, places=5)
        self.assertAlmostEqual(resultado.loc['a_3', 'Media'], 3.0, places=5)

    def test_erro_estatistico_positivo(self):
        """S_err deve ser >= 0 para todos os pontos."""
        resultado = calcular_estatisticas(_df_padrao())
        self.assertTrue((resultado['S_err'] >= 0).all())

    def test_erro_total_maior_ou_igual_instrumental(self):
        """T_err deve ser sempre >= erro instrumental (pois T_err inclui S_err)."""
        resultado = calcular_estatisticas(_df_padrao())
        # Para o grupo 'a' o erro instrumental eh 0.10
        a_rows = resultado[resultado['Dados'].str.startswith('a')]
        self.assertTrue((a_rows['T_err'] >= 0.10 - 1e-9).all())

    def test_propagacao_quadratica(self):
        """
        T_err = sqrt(S_err^2 + I_err^2).

        Para a_1: valores = [1.0, 1.1, 0.9]
            media   = 1.0
            desvio  = sqrt(((1.0-1.0)^2 + (1.1-1.0)^2 + (0.9-1.0)^2) / 2)
                    = sqrt(0.02/2) = sqrt(0.01) = 0.1
            S_err   = 0.1 / sqrt(3) ≈ 0.05774
            I_err   = 0.10
            T_err   = sqrt(0.05774^2 + 0.10^2) ≈ 0.11547
        """
        resultado = calcular_estatisticas(_df_padrao())
        resultado = resultado.set_index('Dados')

        s_err = resultado.loc['a_1', 'S_err']
        t_err = resultado.loc['a_1', 'T_err']
        i_err = 0.10

        t_err_esperado = math.sqrt(s_err**2 + i_err**2)
        self.assertAlmostEqual(t_err, t_err_esperado, places=5)

    def test_repeticao_unica_s_err_zero(self):
        """Com apenas uma repeticao, o erro estatistico deve ser 0."""
        resultado = calcular_estatisticas(_df_repeticao_unica())
        resultado = resultado.set_index('Dados')
        self.assertAlmostEqual(resultado.loc['a_1', 'S_err'], 0.0, places=9)

    def test_dataframe_vazio_levanta_excecao(self):
        """DataFrame vazio deve levantar DadosInvalidosException."""
        with self.assertRaises(DadosInvalidosException):
            calcular_estatisticas(pd.DataFrame())


# --------------------------------------------------------------------------- #
#  Ponto de entrada                                                            #
# --------------------------------------------------------------------------- #

if __name__ == '__main__':
    unittest.main(verbosity=2)
