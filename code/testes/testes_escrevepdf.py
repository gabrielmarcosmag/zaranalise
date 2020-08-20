"""
@autor: Gabriel Marcos Magalhães
Arquivo onde estão escritos os testes relacionados as funções responsáveis por escrever um 
arquivo PDF com informações que estão escritas no arquivo src/escreve_pdf.py
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

from escreve_pdf import * # biblioteca criada para manipulação das datas
from unittest import TestCase, main # biblioteca utilizada nos TDDs

class TesteMm2p(TestCase):
    def teste_conversao_de_mm_para_pt(self):
        """
        Testando a conversão de um valor em milimetro para ponto
        """
        entrada = [1,1.5,2,2.4,3.1]
        saida = [2.834645669,4.251968504,5.669291339,6.803149606,8.787401575]
        print(len(entrada))
        for i in range(len(entrada)):
            with self.subTest(entrada=entrada):
                # Precisão de 4 casas decimais
                self.assertEqual(round(mm2p(entrada[i]),4),round(saida[i],4))

class TesteEscrevePDF(TestCase):
    def teste_relatorio_gerado_com_sucesso(self):
        """
        Testando a geração do arquivo PDF verificando a existência do arquivo
        """
        filename = "relatorio_teste.pdf"
        tabela = '|Num Linha | Texto| \n | 1 | linha 1| \n | 2 | linha 2| \n | 3 | linha 3| \n'
        linhas = ['linha1','linha2','linha3','linha4',tabela]
        relatorio(linhas,filename)
        try:
            with open(filename, 'r') as f:
                arquivo_existe =  True
        except FileNotFoundError as e:
            arquivo_existe =  False
        except IOError as e:
            arquivo_existe =  False
        self.assertTrue(arquivo_existe)

        os.remove(filename)

if __name__ == '__main__':
    main()