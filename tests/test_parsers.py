"""
Testes unitários para módulo de parsers
"""

import unittest
from src.utils.parsers import (
    extrair_prefixo,
    eh_erro_instrumental
)

class TestParsers(unittest.TestCase):
    """Testes para funções de parsing"""
    
    def test_extrair_prefixo_simples(self):
        """Testa extração de prefixo simples"""
        self.assertEqual(extrair_prefixo('x1'), 'x')
        self.assertEqual(extrair_prefixo('y2'), 'y')
        self.assertEqual(extrair_prefixo('temp3'), 'temp')

    def test_extrair_prefixo_complexo(self):
        """Testa extração com nomes mais complexos"""
        self.assertEqual(extrair_prefixo('temperatura1'), 'temperatura')
        self.assertEqual(extrair_prefixo('pressao2'), 'pressao')
    
    def test_extrair_prefixo_invalido(self):
        """Testa casos inválidos"""
        self.assertIsNone(extrair_prefixo('123'))
        self.assertIsNone(extrair_prefixo(''))
        self.assertIsNone(extrair_prefixo(None))
    
    def test_eh_erro_instrumental_valido(self):
        """Testa detecção de colunas de erro"""
        self.assertTrue(eh_erro_instrumental('xerr_instr'))
        self.assertTrue(eh_erro_instrumental('yerr_instr'))
        self.assertTrue(eh_erro_instrumental('XERR_INSTR'))  # Case insensitive
    
    def test_eh_erro_instrumental_invalido(self):
        """Testa casos que não são erro instrumental"""
        self.assertFalse(eh_erro_instrumental('x1'))
        self.assertFalse(eh_erro_instrumental('erro'))
        self.assertFalse(eh_erro_instrumental(''))
        self.assertFalse(eh_erro_instrumental(None))

if __name__ == '__main__':
    unittest.main()