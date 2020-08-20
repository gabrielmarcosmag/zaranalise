"""
@autor: Gabriel Marcos Magalhães
Arquivo onde estão escritos os testes relacionados as funções responsáveis pela manipulação de datas
que estão escritas no arquivo src/data.py
"""
# Atribuição do diretório src, onde está o código
try:
    import sys
    import os

    sys.path.append(
        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),'../src'
            )
        )
    )
except:
    raise

from data import * # biblioteca criada para manipulação das datas
from unittest import TestCase, main # biblioteca utilizada nos TDDs
from datetime import datetime # Biblioteca para formatação da data
from unittest.mock import patch # Biblioteca para simular comando

class TesteValidaData(TestCase):
    """
    Testes escritos para a função valida_data
    """
    def teste_data_vazia(self):
        """
        Testando a validade de uma data vazia
        """
        data = ''
        self.assertFalse(valida_data(data))

    def teste_datas_com_espaco(self):
        """
        Testando a validade de datas com espaço
        """
        entradas = ('03/ 5/2019',' 3/05/2019','03/05/2 19',' 03/05/2019','03/05/2019 ')
        for entrada in entradas:
            with self.subTest(entrada=entrada):
                self.assertFalse(valida_data(entrada),msg = f'{entrada} não retornou o esperado')

    def teste_datas_sem_barra(self):
        """
        Testando a validade de datas com separadores que não sejam barras
        """
        entradas = ('03-05-2019','03.05.2019','03a05a2019')
        for entrada in entradas:
            with self.subTest(entrada=entrada):
                self.assertFalse(valida_data(entrada),msg = f'{entrada} não retornou o esperado')

    def teste_datas_em_outros_formatos(self):
        """
        Testando a validade de data com formatos diferentes de DD/MM/AAAA
        """
        entradas = ('2019/05/03','03/14/2019')
        for entrada in entradas:
            with self.subTest(entrada=entrada):
                self.assertFalse(valida_data(entrada),msg = f'{entrada} não retornou o esperado')

    def teste_dia_29_de_fevereiro_em_anos_nao_bissextos(self):
        """
        Testando a validade do dia 29 de fevereiro em anos que não são bissextos
        """
        entradas = ('29/02/2019','29/02/2018','29/02/2017')
        for entrada in entradas:
            with self.subTest(entrada=entrada):
                self.assertFalse(valida_data(entrada),msg = f'{entrada} não retornou o esperado')

    def teste_dia_29_de_fevereiro_em_anos_bissextos(self):
        """
        Testando a validade do dia 29 de fevereiro em anos que são bissextos
        """
        entradas = ('29/02/2020','29/02/2016','29/02/2012')
        for entrada in entradas:
            with self.subTest(entrada=entrada):
                self.assertIsNot(valida_data(entrada),False,msg = f'{entrada} não retornou o esperado')

    def teste_dia_31_em_dias_que_nao_tem(self):
        """
        Testando a validade do dia 31 em meses que não possuem dia 31
        """
        entradas = ('31/02/2016','31/04/2016','31/06/2016','31/09/2016','31/11/2016')
        for entrada in entradas:
            with self.subTest(entrada=entrada):
                self.assertFalse(valida_data(entrada),msg = f'{entrada} não retornou o esperado')

    def teste_datas_que_nao_existem(self):
        """
        Testando a validade de datas inexistentes
        """
        entradas = ('32/01/2019','30/02/2019','29/14/2017')
        for entrada in entradas:
            with self.subTest(entrada=entrada):
                self.assertFalse(valida_data(entrada),msg = f'{entrada} não retornou o esperado')

    def teste_datas_com_caracteres_invalidos(self):
        """
        Testando a validade de datas com caracteres inválidos
        """
        entradas = ('32/0a/2019','30/0-/2019','29//10/2017','#3/\t/2020')
        for entrada in entradas:
            with self.subTest(entrada=entrada):
                self.assertFalse(valida_data(entrada),msg = f'{entrada} não retornou o esperado')

    def teste_retorno_esperado(self):
        """
        Testando a conversão do formarto fornecido pelo usuário no formato que será usado nas 
        operações, que é o valor retornado pela função valida_data
        """
        entrada = '06/04/2012'
        saida = datetime(2012,4,6).date()
        self.assertEqual(valida_data(entrada),saida,msg = f'{entrada} não retornou o esperado')

class TesteValidaIntervalo(TestCase):
    def setUp(self):
        """
        Defininição do intervalo de datas com dados disponíveis no dataframe
        """
        self.min_data = '2012-03-08'
        self.max_data = '2020-01-14'

    def teste_data_minima_escolhida_menor_que_data_minima_do_intervalo_possivel(self):
        """
        Testando um intervalo inválido onde a data mínima fornecida pelo usuário é menor que a data mínima onde
        existem dados disponíveis no dataframe
        """
        min_entrada = datetime(2012,2,6).date()
        max_entrada = datetime(2012,8,6).date()
        self.assertFalse(valida_intervalo(self.min_data,self.max_data,min_entrada,max_entrada),msg = f'{min_entrada} não retornou o esperado')

    def teste_data_maxima_escolhida_maior_que_data_maxima_do_intervalo_possivel(self):
        """
        Testando um intervalo inválido onde a data máxima fornecida pelo usuário é maior que a data máxima onde
        existem dados disponíveis no dataframe
        """
        min_entrada = datetime(2012,4,6).date()
        max_entrada = datetime(2021,8,6).date()
        self.assertFalse(valida_intervalo(self.min_data,self.max_data,min_entrada,max_entrada),msg = f'{max_entrada} não retornou o esperado')

    def teste_data_maxima_escolhida_menor_que_data_minima_escolhida(self):
        """
        Testando um intervalo inválido onde a data máxima fornecida pelo usuário é menor que a data mínima
        fornecida pelo usuário
        """
        min_entrada = datetime(2012,4,6).date()
        max_entrada = datetime(2012,4,4).date()
        self.assertFalse(valida_intervalo(self.min_data,self.max_data,min_entrada,max_entrada),msg = f'{min_entrada} e {max_entrada} não retornou o esperado')

    def teste_data_maxima_escolhida_igual_a_data_minima_escolhida(self):
        """
        Testando um intervalo inválido onde a data máxima fornecida pelo usuário é menor que a data mínima
        fornecida pelo usuário
        """
        min_entrada = datetime(2012,4,6).date()
        max_entrada = datetime(2012,4,6).date()
        self.assertFalse(valida_intervalo(self.min_data,self.max_data,min_entrada,max_entrada),msg = f'{min_entrada} e {max_entrada} não retornou o esperado')

    def teste_intervalo_valido(self):
        """
        Testando um intervalo válido
        """
        min_entrada = datetime(2012,4,6).date()
        max_entrada = datetime(2012,8,4).date()
        self.assertTrue(valida_intervalo(self.min_data,self.max_data,min_entrada,max_entrada),msg = f'{min_entrada} e {max_entrada} não retornou o esperado')

class TesteLeData(TestCase):
    """
    Testes escritos para a função le_data
    """
    def setUp(self):
        """
        Defininição do intervalo de datas com dados disponíveis no dataframe
        """
        self.min_data = '2012-03-08'
        self.max_data = '2020-01-14'

    def runTest(self, data1, data2, retorno_esperado):
        """
        Simulação dos comandos input
        """
        with patch('builtins.input', side_effect=[data1,data2]) as fake_out:
            self.assertEqual(le_data(self.min_data,self.max_data), retorno_esperado, msg=f'{data1} e {data2} não retornaram o esperado')

    def teste_primeira_data_inserida_invalida(self):
        """
        Testando quando a primeira data inserida pelo usuário é inválida
        """
        data1 = '30/02/2019'
        data2 = '05/08/2019'
        self.runTest(data1,data2,False)

    def teste_segunda_data_inserida_invalida(self):
        """
        Testando quando a segunda data inserida pelo usuário é inválida
        """
        data1 = '05/02/2019'
        data2 = '32/08/2019'
        self.runTest(data1,data2,False)

    def teste_intervalo_inserido_invalido(self):
        """
        Testando quando as datas inseridas pelo usuário são válidas mas o intervalo é inválido
        """
        data1 = '30/09/2019'
        data2 = '05/08/2019'
        self.runTest(data1,data2,False)

    def teste_datas_validas_e_intervalo_inserido_valido(self):
        """
        Testando quando as datas inseridas pelo usuário são válidas e o intervalo é válido
        """
        data1 = '30/05/2019'
        data2 = '05/08/2019'
        saida = ['2019-05-30','2019-08-05']
        self.runTest(data1,data2,saida)

class TestePdata(TestCase):
    """
    Testes escritos para a função pdata
    """
    def teste_datas_com_formato_invalido_para_a_funcao(self):
        """
        Testando argumentos inválidos para a função
        """
        entradas = ('03/05/2019','03-05-2019','2018-07-14 ')
        for entrada in entradas:
            with self.subTest(entrada=entrada):
                self.assertFalse(pdata(entrada),msg = f'{entrada} não retornou o esperado')

    def teste_datas_com_formato_valido_para_a_funcao(self):
        """
        Testando argumentos válidos para a função com retorno esperado
        """
        entradas = ('2019-03-05','2018-07-14')
        for entrada in entradas:
            with self.subTest(entrada=entrada): 
                self.assertRegex(pdata(entrada),r'^\d{2}\/\d{2}\/\d{4}$')


if __name__ == '__main__':
    main()