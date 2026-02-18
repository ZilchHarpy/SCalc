"""
Testes para o modulo de parsers (parsers.py).

Funcoes testadas:
    extrair_prefixo(nome)       -> str | None
    eh_erro_instrumental(nome)  -> bool
    contar(prefixo, lista)      -> int

AVISO — falso positivo conhecido em eh_erro_instrumental():
    A funcao classifica uma coluna como erro instrumental quando o nome contem
    simultaneamente um indicador de erro ("err"/"error"/"erro") E a letra "i"
    em qualquer posicao (nao como token isolado). Isso causa falsos positivos
    em nomes como "distancia_err" ou "medicao_error", pois ambos contem a
    letra 'i' na parte descritiva do nome. O teste test_falso_positivo_letra_i
    documenta esse comportamento para rastrear futuras correcoes.
"""

import unittest
from src.utils.parsers import extrair_prefixo, eh_erro_instrumental, contar


# --------------------------------------------------------------------------- #
#  TestExtrairPrefixo                                                          #
# --------------------------------------------------------------------------- #

class TestExtrairPrefixo(unittest.TestCase):
    """Testes para extrair_prefixo()."""

    def test_prefixo_letra_unica(self):
        """Uma letra seguida de numero deve retornar a letra."""
        self.assertEqual(extrair_prefixo('x1'), 'x')
        self.assertEqual(extrair_prefixo('y2'), 'y')
        self.assertEqual(extrair_prefixo('z9'), 'z')

    def test_prefixo_multiplas_letras(self):
        """Multiplas letras seguidas de numero devem retornar todas as letras."""
        self.assertEqual(extrair_prefixo('temp3'),        'temp')
        self.assertEqual(extrair_prefixo('temperatura1'), 'temperatura')
        self.assertEqual(extrair_prefixo('pressao2'),     'pressao')

    def test_prefixo_com_underscore(self):
        """Formato 'prefixo_n' deve retornar apenas o prefixo alfabetico."""
        self.assertEqual(extrair_prefixo('a_1'),    'a')
        self.assertEqual(extrair_prefixo('temp_2'), 'temp')

    def test_apenas_letras_sem_numero(self):
        """String somente com letras deve retornar a string completa."""
        self.assertEqual(extrair_prefixo('abc'), 'abc')

    def test_entradas_invalidas_retornam_none(self):
        """Entradas sem prefixo alfabetico valido devem retornar None."""
        self.assertIsNone(extrair_prefixo('123'))
        self.assertIsNone(extrair_prefixo(''))
        self.assertIsNone(extrair_prefixo(None))

    def test_espacos_no_inicio_sao_ignorados(self):
        """Espacos iniciais devem ser ignorados (strip interno)."""
        self.assertEqual(extrair_prefixo('  x1'), 'x')

    def test_maiusculas_preservadas(self):
        """O prefixo deve preservar o case original."""
        self.assertEqual(extrair_prefixo('Temp1'), 'Temp')
        self.assertEqual(extrair_prefixo('PRESSAO2'), 'PRESSAO')


# --------------------------------------------------------------------------- #
#  TestEhErroInstrumental                                                      #
# --------------------------------------------------------------------------- #

class TestEhErroInstrumental(unittest.TestCase):
    """Testes para eh_erro_instrumental()."""

    # -- casos verdadeiros -------------------------------------------------- #

    def test_formatos_tipicos_do_modelo(self):
        """Formatos usados no modelo de tabela do SCalc devem retornar True."""
        self.assertTrue(eh_erro_instrumental('I_err'))
        self.assertTrue(eh_erro_instrumental('xerr_instr'))
        self.assertTrue(eh_erro_instrumental('yerr_instr'))

    def test_insensibilidade_a_maiusculas(self):
        """A deteccao deve ser insensivel a maiusculas."""
        self.assertTrue(eh_erro_instrumental('I_ERR'))
        self.assertTrue(eh_erro_instrumental('XERR_INSTR'))
        self.assertTrue(eh_erro_instrumental('i_Err'))

    def test_variantes_de_error(self):
        """Variacoes de 'err': 'error' e 'erro' tambem devem ser detectadas."""
        self.assertTrue(eh_erro_instrumental('i_error'))
        self.assertTrue(eh_erro_instrumental('i_erro'))

    def test_variantes_de_instrumental(self):
        """Variacoes de 'i': 'instr', 'ins', 'instrumental' devem ser detectadas."""
        self.assertTrue(eh_erro_instrumental('instr_err'))
        self.assertTrue(eh_erro_instrumental('ins_error'))
        self.assertTrue(eh_erro_instrumental('instrumental_err'))

    # -- casos falsos -------------------------------------------------------- #

    def test_dados_normais_retornam_false(self):
        """Colunas de dados comuns nao devem ser classificadas como erro."""
        self.assertFalse(eh_erro_instrumental('x1'))
        self.assertFalse(eh_erro_instrumental('y2'))
        self.assertFalse(eh_erro_instrumental('temperatura3'))
        self.assertFalse(eh_erro_instrumental('1'))
        self.assertFalse(eh_erro_instrumental('Dados'))

    def test_erro_sem_indicador_instrumental(self):
        """Coluna com 'err' mas sem indicador de instrumental deve retornar False."""
        # 'erro' presente, mas sem 'i', 'instr', etc. em nenhuma posicao
        # 'erro' nao contem 'i' -> False
        self.assertFalse(eh_erro_instrumental('erro'))
        self.assertFalse(eh_erro_instrumental('error'))

    def test_entradas_invalidas_retornam_false(self):
        """Entradas nao-string devem retornar False sem lancar excecao."""
        self.assertFalse(eh_erro_instrumental(''))
        self.assertFalse(eh_erro_instrumental(None))
        self.assertFalse(eh_erro_instrumental(42))

    # -- falso positivo documentado ----------------------------------------- #

    def test_falso_positivo_letra_i(self):
        """
        COMPORTAMENTO CONHECIDO — nao e um teste de corretude, mas de regressao.

        Colunas como 'distancia_err' e 'medicao_error' contem a letra 'i'
        na parte descritiva do nome e por isso sao incorretamente classificadas
        como erros instrumentais. Este teste documenta o comportamento atual
        para que qualquer correcao futura seja detectada.

        Se este teste comecar a FALHAR, significa que o bug foi corrigido —
        o que e desejavel. Atualize-o para refletir o comportamento correto.
        """
        # Estes deveriam ser False, mas retornam True pelo bug descrito acima.
        resultado_distancia = eh_erro_instrumental('distancia_err')
        resultado_medicao   = eh_erro_instrumental('medicao_error')

        # Documentar que o falso positivo existe:
        self.assertTrue(
            resultado_distancia,
            "Se chegou aqui, o falso positivo de 'distancia_err' foi corrigido. "
            "Atualize este teste para assertFalse."
        )
        self.assertTrue(
            resultado_medicao,
            "Se chegou aqui, o falso positivo de 'medicao_error' foi corrigido. "
            "Atualize este teste para assertFalse."
        )


# --------------------------------------------------------------------------- #
#  TestContar                                                                  #
# --------------------------------------------------------------------------- #

class TestContar(unittest.TestCase):
    """Testes para contar()."""

    def setUp(self):
        self.lista = ['a_1', 'a_2', 'a_3', 'b_1', 'b_2', 'temperatura_1']

    def test_conta_prefixo_simples(self):
        """Deve contar apenas os itens que comecam com o prefixo dado."""
        self.assertEqual(contar('a', self.lista), 3)
        self.assertEqual(contar('b', self.lista), 2)

    def test_conta_prefixo_multiplas_letras(self):
        """Prefixos com mais de uma letra devem funcionar corretamente."""
        self.assertEqual(contar('temperatura', self.lista), 1)

    def test_prefixo_ausente_retorna_zero(self):
        """Prefixo que nao existe na lista deve retornar 0."""
        self.assertEqual(contar('z', self.lista), 0)

    def test_nao_conta_substring_parcial(self):
        """
        'a' nao deve contar 'temperatura_1' mesmo contendo a letra 'a',
        pois o separador (_, espaco, -) ou fim de string e exigido.
        """
        # 'temperatura_1'.startswith('a_') -> False -> nao deve ser contado
        self.assertEqual(contar('a', ['temperatura_1', 'a_1']), 1)

    def test_lista_vazia_retorna_zero(self):
        """Lista vazia deve sempre retornar 0."""
        self.assertEqual(contar('a', []), 0)


# --------------------------------------------------------------------------- #
#  Ponto de entrada                                                            #
# --------------------------------------------------------------------------- #

if __name__ == '__main__':
    unittest.main(verbosity=2)
