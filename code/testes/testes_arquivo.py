
"""
@autor: Gabriel Marcos Magalhães
Arquivo onde estão escritos os testes relacionados as funções responsáveis pela manipulação de arquivos
de entrada de dados que estão escritas no arquivo src/arquivo.py
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
from unittest import TestCase, main # biblioteca utilizada nos TDDs
from arquivo import * # biblioteca criada para manipulação dos arquivos de dados
import pandas as pd # Importação da biblioteca pandas (manipulação de dataframes)

class TesteExistenciaDeArquivo(TestCase):
    """
    Testes escritos para a função existencia_arquivo
    """
    def teste_tentando_ler_arquivos_inexistentes(self):
        """
        Testando a tentativa de leitura de arquivos inexistentes
        """
        entradas = ('qualquer_arquivo.dat','arquivo2.xlsx','cotas_cdi_dados.xlsx')
        for entrada in entradas:
            with self.subTest(entrada=entrada):
                self.assertFalse(existencia_arquivo(entrada),msg = f'{entrada} não retornou o esperado')
    
    def teste_tentando_ler_arquivos_existentes(self):
        """
        Testando a tentativa de leitura de arquivos existentes
        """
        entradas = ('../dados/zarathustra.csv','../dados/cotas_cdi_dados.xlsx','../dados/cdi.csv')
        for entrada in entradas:
            with self.subTest(entrada=entrada):
                self.assertTrue(existencia_arquivo(entrada),msg = f'{entrada} não retornou o esperado')

class TesteRemovePorcentagem(TestCase):
    """
    Testes escritos para a função remove_porcentagem
    """
    def teste_retirando_porcentagem_de_uma_serie_pd(self):
        """
        Testando a tentativa de remover porcentagem de uma série que possui o 
        simbolo de porcentagem e deve ser modificada
        """
        entrada = pd.Series(['1.0%','2.0%','30.5%','0.3%','0.0%','100.0%'])
        saida = pd.Series([0.01,0.02,0.305,0.003,0.0,1.0])
        self.assertEqual(remove_porcentagem(entrada).all(),saida.all())

    def teste_com_serie_sem_porcentagem_que_nao_deve_ser_modificada(self):
        """
        Testando a tentativa de remover porcentagem de uma série que não possui o 
        simbolo de porcentagem
        """
        entrada = pd.Series(['1.0','2.0','30.5','0.3','0.0','100.0'])
        self.assertEqual(remove_porcentagem(entrada).all(),entrada.all())

    def teste_com_porcentagem_nao_no_final_que_nao_deve_ser_modificada(self):
        """
        Testando a tentativa de remover porcentagem de um formato válido
        """
        entrada = pd.Series(['a%b','2.0%3','10a%'])
        self.assertEqual(remove_porcentagem(entrada).all(),entrada.all())

class TesteRemoveHora(TestCase):
    """
    Testes escritos para a função remove_hora
    """
    def teste_retirando_hora_de_uma_serie_pd_de_datas(self):
        """
        Testando a remoção dos dados de hora de uma série com datas no formato
        AAAA-MM-DD HH:MM:SS
        """
        entrada = pd.Series(['1995-02-07 00:00:00','1996-03-04 00:00:00','2012-04-06 00:00:00'])
        saida = pd.Series(['1995-02-07','1996-03-04','2012-04-06'])
        self.assertEqual(remove_hora(entrada).all(),saida.all())

    def teste_com_serie_de_datas_sem_hora_que_nao_deve_ser_modificada(self):
        """
        Testando se uma série com datas no formato AAAA-MM-DD se mantém inalterada ao ser
        submetida a função
        """
        entrada = pd.Series(['1995-02-07','1996-03-04','2012-04-06'])
        self.assertEqual(remove_hora(entrada).all(),entrada.all())

class TesteLeExcel(TestCase):
    """
    Testes escritos para a função le_excel
    """
    def teste_tentando_ler_arquivos_inexistentes_com_le_excel(self):
        """
        Testando a tentativa de leitura de arquivos inexistentes com a função le_excel
        """
        entradas = ('qualquer_arquivo.dat','arquivo2.xlsx','cotas_cdi_dados.xlsx')
        for entrada in entradas:
            with self.subTest(entrada=entrada):
                self.assertFalse(le_excel(entrada),msg = f'{entrada} não retornou o esperado')

    def teste_arquivo_existe_mas_nao_esta_adequado_formato_excel_exigido(self):
        """
        Testando a tentativa de leitura de um arquivo existente mas que não atende aos requisitos 
        para ser lido com a função le_excel
        """
        arq = "../dados/cdi.csv"
        self.assertFalse(le_excel(arq))

    def teste_arquivo_excel_correto(self):
        """
        Testando a tentativa de leitura de um arquivo existente e válido para a função le_excel
        """
        arq = "../dados/cotas_cdi_dados.xlsx"
        self.assertNotEqual(le_excel(arq),False)


class TesteLeCsv(TestCase):
    """
    Testes escritos para a função le_csv
    """
    def teste_tentando_ler_arquivos_inexistentes_com_lecsv(self):
        """
        Testando a tentativa de leitura de arquivos inexistentes com a função le_csv
        """
        entradas = ('qualquer_arquivo.dat','arquivo2.xlsx','cotas_cdi_dados.xlsx','arquivo1.csv')
        for entrada in entradas:
            with self.subTest(entrada=entrada):
                self.assertFalse(le_csv(entrada),msg = f'{entrada} não retornou o esperado')

    def teste_arquivo_existe_mas_nao_esta_adequado_formato_csv_exigido(self):
        """
        Testando a tentativa de leitura de arquivos existentes mas que não atendem aos requisitos 
        para ser lido com a função le_csv
        """
        arq = ["../dados/cotas_cdi_dados.xlsx","../dados/cotas_cdi_dados.xlsx"]
        self.assertFalse(le_csv(arq))

    def teste_passando_somente_um_arquivo(self):
        """
        Testando a tentativa de leitura de somente um arquvio com a função le_csv quando ela necessita de dois
        """
        arq = ["../dados/zarathustra.csv"]
        self.assertFalse(le_csv(arq))

    def teste_passando_dois_arquivos_existentes_um_arquivo_valido_e_um_invalido(self):
        """
        Testando a tentativa de leitura de arquivos existentes onde um não atende aos requisitos 
        para ser lido com a função le_csv
        """
        arq = ["../dados/zarathustra.csv","../dados/cotas_cdi_dados.xlsx"]
        self.assertFalse(le_csv(arq))

    def teste_arquivos_csv_corretos(self):
        """
        Testando a tentativa de leitura de arquivos existentes e válidos para a função le_csv
        """
        arq = ["../dados/zarathustra.csv", "../dados/cdi.csv"]
        self.assertNotEqual(le_csv(arq),False)

class TesteLeArq(TestCase):
    """
    Testes escritos para a função le_arq
    """
    def teste_formatos_invalidos(self):
        """
        Testando formatos inválidos para a função le_arq
        """
        entradas = ('dat','txt','xls','outro','pdf',10)
        for entrada in entradas:
            with self.subTest(entrada=entrada):
                self.assertFalse(le_arq(entrada),msg = f'{entrada} não retornou o esperado')

    def teste_lendo_formatos_existentes(self):
        """
        Testando se a função le_arq não retorna false para formatos válidos "xlsx" e "csv"
        """
        entradas = ('xlsx','csv')
        for entrada in entradas:
            with self.subTest(entrada=entrada):
                self.assertNotEqual(type(le_arq(entrada)),bool)

if __name__ == '__main__':
    main()