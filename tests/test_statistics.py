"""
Testes para o modulo de estatistica (statistics.py).

Estrutura esperada pelo particionar():
    - Coluna cujo nome contenha 'dados' (case-insensitive): identificadores
      no formato <prefixo>_<n>, ex: a_1, a_2, b_1.
    - Colunas numericas (qualquer nome que nao seja 'dados' nem erro):
      cada coluna e uma repeticao da medicao.
    - Coluna de erro instrumental: nome deve conter simultaneamente um
      indicador de erro ('err'/'error'/'erro') E um indicador de instrumental
      como token isolado ('i', 'instr', 'ins', 'instrumental').

calcular_estatisticas() retorna pd.DataFrame com colunas:
    ['Dados', 'Media', 'S_err', 'T_err']
"""

import math
import unittest

import pandas as pd

from src.core import calcular_estatisticas, particionar
from src.core.exceptions import DadosInvalidosException


# --------------------------------------------------------------------------- #
#  Fixtures                                                                    #
# --------------------------------------------------------------------------- #

def _df_padrao():
    """
    DataFrame canonico com dois grupos (a, b) e tres repeticoes por ponto.

    Medias esperadas:
        a_1 = mean(1.0, 1.1, 0.9) = 1.0
        a_2 = mean(2.0, 2.1, 1.9) = 2.0
        a_3 = mean(3.0, 3.1, 2.9) = 3.0
        b_1 = mean(2.0, 2.1, 1.9) = 2.0
        b_2 = mean(4.0, 4.1, 3.9) = 4.0
        b_3 = mean(6.0, 6.1, 5.9) = 6.0

    Erros instrumentais: grupo a = 0.10, grupo b = 0.20
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


def _df_ordem_invertida():
    """
    Mesmo conteudo de _df_padrao(), mas com I_err ANTES de Dados.
    Testa a independencia de ordem das colunas no particionar().
    """
    return pd.DataFrame({
        'I_err': [0.10,  0.10,  0.10,  0.20,  0.20,  0.20],
        'Dados': ['a_1', 'a_2', 'a_3', 'b_1', 'b_2', 'b_3'],
        '1':     [1.0,   2.0,   3.0,   2.0,   4.0,   6.0],
        '2':     [1.1,   2.1,   3.1,   2.1,   4.1,   6.1],
        '3':     [0.9,   1.9,   2.9,   1.9,   3.9,   5.9],
    })


# --------------------------------------------------------------------------- #
#  TestParticionar                                                              #
# --------------------------------------------------------------------------- #

class TestParticionar(unittest.TestCase):
    """Testes para particionar()."""

    def test_retorna_tres_valores(self):
        r = particionar(_df_padrao())
        self.assertIsInstance(r, tuple)
        self.assertEqual(len(r), 3)

    def test_prefixos_extraidos(self):
        dados_brutos, _, _ = particionar(_df_padrao())
        self.assertIn('a', dados_brutos)
        self.assertIn('b', dados_brutos)

    def test_chaves_internas(self):
        dados_brutos, _, _ = particionar(_df_padrao())
        self.assertSetEqual(set(dados_brutos['a'].keys()), {'a_1', 'a_2', 'a_3'})
        self.assertSetEqual(set(dados_brutos['b'].keys()), {'b_1', 'b_2', 'b_3'})

    def test_valores_corretos(self):
        dados_brutos, _, _ = particionar(_df_padrao())
        vals = dados_brutos['a']['a_1']
        self.assertAlmostEqual(sum(vals) / len(vals), 1.0, places=5)

    def test_erros_instrumentais_prefixos(self):
        _, erros_instr, _ = particionar(_df_padrao())
        self.assertIn('a', erros_instr)
        self.assertIn('b', erros_instr)

    def test_erros_instrumentais_valores(self):
        _, erros_instr, _ = particionar(_df_padrao())
        self.assertAlmostEqual(erros_instr['a']['a_1'], 0.10, places=5)
        self.assertAlmostEqual(erros_instr['b']['b_1'], 0.20, places=5)

    def test_dados_keys_contagem(self):
        _, _, dados_keys = particionar(_df_padrao())
        self.assertEqual(dados_keys['a'], 3)
        self.assertEqual(dados_keys['b'], 3)

    def test_dataframe_vazio_levanta_excecao(self):
        with self.assertRaises(DadosInvalidosException):
            particionar(pd.DataFrame())

    def test_nan_em_repeticoes_ignorado(self):
        """Celulas NaN em colunas de repeticao devem ser ignoradas."""
        df = pd.DataFrame({
            'Dados': ['a_1', 'a_2', 'b_1', 'b_2'],
            'I_err': [0.05,  0.05,  0.10,  0.10],
            '1':     [1.0,   2.0,   2.0,   4.0],
            '2':     [1.1,   None,  2.1,   None],
        })
        dados_brutos, _, _ = particionar(df)
        self.assertIn('a', dados_brutos)

    # -- bug corrigido: independencia de ordem das colunas ------------------ #

    def test_ordem_de_colunas_nao_afeta_resultado(self):
        """
        Bug corrigido: se I_err viesse antes de Dados, o mapeamento posicional
        entre erros e identificadores falhava com TypeError (lista como chave
        de dict) ou produzia mapeamento errado silenciosamente.

        Apos a correcao (duas passagens), a ordem das colunas nao importa.
        """
        db_normal,  ei_normal,  _ = particionar(_df_padrao())
        db_invertido, ei_invertido, _ = particionar(_df_ordem_invertida())

        # Mesmos prefixos
        self.assertSetEqual(set(db_normal.keys()), set(db_invertido.keys()))

        # Mesmas chaves e valores
        for prefixo in db_normal:
            self.assertSetEqual(
                set(db_normal[prefixo].keys()),
                set(db_invertido[prefixo].keys()),
            )
            for chave in db_normal[prefixo]:
                self.assertAlmostEqual(
                    sum(db_normal[prefixo][chave]) / len(db_normal[prefixo][chave]),
                    sum(db_invertido[prefixo][chave]) / len(db_invertido[prefixo][chave]),
                    places=5,
                )

        # Mesmos erros instrumentais
        for prefixo in ei_normal:
            for chave in ei_normal[prefixo]:
                self.assertAlmostEqual(
                    ei_normal[prefixo][chave],
                    ei_invertido[prefixo][chave],
                    places=5,
                )

    def test_i_err_antes_de_dados_nao_crasha(self):
        """
        Garante que a ordem I_err -> Dados nao levanta TypeError.
        (Antes da correcao, lista era usada como chave de dict.)
        """
        try:
            particionar(_df_ordem_invertida())
        except TypeError as e:
            self.fail(
                f"particionar() levantou TypeError com colunas fora de ordem: {e}"
            )


# --------------------------------------------------------------------------- #
#  TestCalcularEstatisticas                                                    #
# --------------------------------------------------------------------------- #

class TestCalcularEstatisticas(unittest.TestCase):
    """Testes para calcular_estatisticas()."""

    def test_retorna_dataframe(self):
        self.assertIsInstance(calcular_estatisticas(_df_padrao()), pd.DataFrame)

    def test_colunas_presentes(self):
        df = calcular_estatisticas(_df_padrao())
        for col in ('Dados', 'Media', 'S_err', 'T_err'):
            self.assertIn(col, df.columns)

    def test_numero_de_linhas(self):
        """6 pontos no total: 3 de 'a' + 3 de 'b'."""
        self.assertEqual(len(calcular_estatisticas(_df_padrao())), 6)

    def test_medias_corretas(self):
        df = calcular_estatisticas(_df_padrao()).set_index('Dados')
        self.assertAlmostEqual(df.loc['a_1', 'Media'], 1.0, places=5)
        self.assertAlmostEqual(df.loc['a_2', 'Media'], 2.0, places=5)
        self.assertAlmostEqual(df.loc['a_3', 'Media'], 3.0, places=5)
        self.assertAlmostEqual(df.loc['b_3', 'Media'], 6.0, places=5)

    def test_erro_estatistico_nao_negativo(self):
        df = calcular_estatisticas(_df_padrao())
        self.assertTrue((df['S_err'] >= 0).all())

    def test_erro_total_maior_ou_igual_instrumental(self):
        df = calcular_estatisticas(_df_padrao()).set_index('Dados')
        for chave in ('a_1', 'a_2', 'a_3'):
            self.assertGreaterEqual(df.loc[chave, 'T_err'], 0.10 - 1e-9)
        for chave in ('b_1', 'b_2', 'b_3'):
            self.assertGreaterEqual(df.loc[chave, 'T_err'], 0.20 - 1e-9)

    def test_propagacao_quadratica(self):
        """
        Para a_1: valores = [1.0, 1.1, 0.9], I_err = 0.10
            desvio = sqrt(((0)^2 + (0.1)^2 + (-0.1)^2) / 2) = 0.1
            S_err  = 0.1 / sqrt(3)
            T_err  = sqrt(S_err^2 + 0.10^2)
        """
        df = calcular_estatisticas(_df_padrao()).set_index('Dados')
        s_err = df.loc['a_1', 'S_err']
        t_err = df.loc['a_1', 'T_err']
        self.assertAlmostEqual(t_err, math.sqrt(s_err ** 2 + 0.10 ** 2), places=5)

    def test_repeticao_unica_s_err_zero(self):
        df = calcular_estatisticas(_df_repeticao_unica()).set_index('Dados')
        self.assertAlmostEqual(df.loc['a_1', 'S_err'], 0.0, places=9)

    def test_dataframe_vazio_levanta_excecao(self):
        with self.assertRaises(DadosInvalidosException):
            calcular_estatisticas(pd.DataFrame())

    def test_resultado_igual_independente_da_ordem_das_colunas(self):
        """calcular_estatisticas deve ser identico com colunas em ordens diferentes."""
        df_normal   = calcular_estatisticas(_df_padrao()).set_index('Dados')
        df_invertido = calcular_estatisticas(_df_ordem_invertida()).set_index('Dados')

        for chave in df_normal.index:
            self.assertAlmostEqual(
                df_normal.loc[chave, 'Media'],
                df_invertido.loc[chave, 'Media'],
                places=5,
            )
            self.assertAlmostEqual(
                df_normal.loc[chave, 'T_err'],
                df_invertido.loc[chave, 'T_err'],
                places=5,
            )


# --------------------------------------------------------------------------- #
#  Ponto de entrada                                                            #
# --------------------------------------------------------------------------- #

if __name__ == '__main__':
    unittest.main(verbosity=2)
