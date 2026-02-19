"""
Testes para o modulo de parsers (parsers.py).

Funcoes testadas:
    extrair_prefixo(nome)       -> str | None
    eh_erro_instrumental(nome)  -> bool
    contar(prefixo, lista)      -> int
"""

import unittest
from src.utils.parsers import extrair_prefixo, eh_erro_instrumental, contar


# --------------------------------------------------------------------------- #
#  TestExtrairPrefixo                                                          #
# --------------------------------------------------------------------------- #

class TestExtrairPrefixo(unittest.TestCase):
    """Testes para extrair_prefixo()."""

    def test_letra_unica(self):
        self.assertEqual(extrair_prefixo('x1'), 'x')
        self.assertEqual(extrair_prefixo('y2'), 'y')
        self.assertEqual(extrair_prefixo('z9'), 'z')

    def test_multiplas_letras(self):
        self.assertEqual(extrair_prefixo('temp3'),        'temp')
        self.assertEqual(extrair_prefixo('temperatura1'), 'temperatura')
        self.assertEqual(extrair_prefixo('pressao2'),     'pressao')

    def test_formato_prefixo_underscore(self):
        """Formato canonico do SCalc: prefixo_n."""
        self.assertEqual(extrair_prefixo('a_1'),    'a')
        self.assertEqual(extrair_prefixo('temp_2'), 'temp')
        self.assertEqual(extrair_prefixo('b_10'),   'b')

    def test_apenas_letras_sem_numero(self):
        """String so com letras retorna a string completa."""
        self.assertEqual(extrair_prefixo('abc'), 'abc')

    def test_entradas_invalidas_retornam_none(self):
        self.assertIsNone(extrair_prefixo('123'))
        self.assertIsNone(extrair_prefixo(''))
        self.assertIsNone(extrair_prefixo(None))
        self.assertIsNone(extrair_prefixo(42))

    def test_espacos_iniciais_ignorados(self):
        """strip() interno deve ignorar espacos no inicio."""
        self.assertEqual(extrair_prefixo('  x1'), 'x')

    def test_maiusculas_preservadas(self):
        self.assertEqual(extrair_prefixo('Temp1'),    'Temp')
        self.assertEqual(extrair_prefixo('PRESSAO2'), 'PRESSAO')


# --------------------------------------------------------------------------- #
#  TestEhErroInstrumental                                                      #
# --------------------------------------------------------------------------- #

class TestEhErroInstrumental(unittest.TestCase):
    """
    Testes para eh_erro_instrumental().

    Logica de deteccao (ambas as condicoes devem ser verdadeiras):
      - Indicador de ERRO por substring: 'err', 'error' ou 'erro' em qualquer
        posicao do nome (captura 'xerr', 'ierr', etc.).
      - Indicador de INSTRUMENTAL por token exato apos split em _-\\s:
        'i', 'instr', 'ins', 'instrumental' ou 'instrument'.
        Token exato evita falso positivo pela letra 'i' embutida em palavras
        como 'distancia' ou 'medicao'.
    """

    # -- verdadeiros -------------------------------------------------------- #

    def test_formatos_canonicos_do_modelo(self):
        """Formatos usados na tabela padrao do SCalc."""
        self.assertTrue(eh_erro_instrumental('I_err'))
        self.assertTrue(eh_erro_instrumental('xerr_instr'))
        self.assertTrue(eh_erro_instrumental('yerr_instr'))

    def test_case_insensitive(self):
        self.assertTrue(eh_erro_instrumental('I_ERR'))
        self.assertTrue(eh_erro_instrumental('XERR_INSTR'))
        self.assertTrue(eh_erro_instrumental('i_Err'))

    def test_variantes_de_error(self):
        self.assertTrue(eh_erro_instrumental('i_error'))
        self.assertTrue(eh_erro_instrumental('i_erro'))

    def test_variantes_de_instrumental(self):
        self.assertTrue(eh_erro_instrumental('instr_err'))
        self.assertTrue(eh_erro_instrumental('ins_error'))
        self.assertTrue(eh_erro_instrumental('instrumental_err'))
        self.assertTrue(eh_erro_instrumental('instrument_err'))

    def test_i_como_token_isolado(self):
        """'i' sozinho como token (entre separadores) deve ser reconhecido."""
        self.assertTrue(eh_erro_instrumental('i_err'))
        self.assertTrue(eh_erro_instrumental('err_i'))
        self.assertTrue(eh_erro_instrumental('x_i_err'))

    # -- falsos ------------------------------------------------------------- #

    def test_dados_normais_retornam_false(self):
        self.assertFalse(eh_erro_instrumental('x1'))
        self.assertFalse(eh_erro_instrumental('y2'))
        self.assertFalse(eh_erro_instrumental('Dados'))
        self.assertFalse(eh_erro_instrumental('1'))
        self.assertFalse(eh_erro_instrumental('temperatura3'))

    def test_erro_sem_indicador_instrumental(self):
        """Contem 'err' mas nenhum token instrumental -> False."""
        self.assertFalse(eh_erro_instrumental('erro'))
        self.assertFalse(eh_erro_instrumental('error'))
        self.assertFalse(eh_erro_instrumental('x_err'))     # 'x' nao e token instr
        self.assertFalse(eh_erro_instrumental('y_error'))   # 'y' nao e token instr
        self.assertFalse(eh_erro_instrumental('val_err'))   # 'val' nao e token instr

    def test_sem_indicador_de_erro(self):
        """Contem token instrumental mas sem 'err' -> False."""
        self.assertFalse(eh_erro_instrumental('i_valor'))
        self.assertFalse(eh_erro_instrumental('instr_dado'))

    def test_entradas_invalidas(self):
        self.assertFalse(eh_erro_instrumental(''))
        self.assertFalse(eh_erro_instrumental(None))
        self.assertFalse(eh_erro_instrumental(42))

    # -- bug corrigido: falso positivo por letra 'i' embutida em palavras -- #

    def test_letra_i_embutida_em_palavra_nao_e_token(self):
        """
        Antes da correcao, nomes como 'distancia_err' retornavam True porque
        'i' aparecia em qualquer posicao da string. Apos a correcao, apenas
        'i' como token isolado (entre separadores) e reconhecido.

        Estes casos DEVEM retornar False.
        """
        self.assertFalse(eh_erro_instrumental('distancia_err'))
        self.assertFalse(eh_erro_instrumental('medicao_error'))
        self.assertFalse(eh_erro_instrumental('via_err'))
        self.assertFalse(eh_erro_instrumental('fisica_erro'))
        self.assertFalse(eh_erro_instrumental('posicao_err'))


# --------------------------------------------------------------------------- #
#  TestContar                                                                  #
# --------------------------------------------------------------------------- #

class TestContar(unittest.TestCase):
    """Testes para contar()."""

    def setUp(self):
        self.lista = ['a_1', 'a_2', 'a_3', 'b_1', 'b_2', 'temperatura_1']

    def test_conta_prefixo_simples(self):
        self.assertEqual(contar('a', self.lista), 3)
        self.assertEqual(contar('b', self.lista), 2)

    def test_conta_prefixo_multiplas_letras(self):
        self.assertEqual(contar('temperatura', self.lista), 1)

    def test_prefixo_ausente_retorna_zero(self):
        self.assertEqual(contar('z', self.lista), 0)

    def test_nao_conta_substring_de_nome_maior(self):
        """
        Bug corrigido: 'temp' nao deve contar 'temperatura_1' mesmo que
        'temperatura' comece com 'temp'. O separador e obrigatorio.
        """
        self.assertEqual(contar('temp',  ['temperatura_1', 'temp_1']), 1)
        self.assertEqual(contar('a',     ['temperatura_1', 'a_1']),    1)
        self.assertEqual(contar('pre',   ['pressao_1', 'pre_1']),      1)

    def test_separadores_reconhecidos(self):
        """Aceita _ espaco - e newline como separadores."""
        lista = ['a_1', 'a 2', 'a-3', 'a\n4', 'ab_1']
        self.assertEqual(contar('a', lista), 4)   # 'ab_1' nao conta

    def test_lista_vazia(self):
        self.assertEqual(contar('a', []), 0)

    def test_prefixo_vazio_nao_conta_nada(self):
        """Prefixo vazio com separador sempre e string vazia+sep, nao deve
        contar items normais."""
        # '' + '_' = '_'; nenhum item comeca com '_'
        self.assertEqual(contar('', ['a_1', 'b_2']), 0)


# --------------------------------------------------------------------------- #
#  Ponto de entrada                                                            #
# --------------------------------------------------------------------------- #

if __name__ == '__main__':
    unittest.main(verbosity=2)
