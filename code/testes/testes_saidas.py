"""
@autor: Gabriel Marcos Magalhães
Arquivo onde estão escritos os testes relacionados as funções responsáveis por saídas de dados
para o usuário que estão escritas no arquivo src/saidas.py
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

from saidas import * # biblioteca criada para manipulação das datas
from unittest import TestCase, main # biblioteca utilizada nos TDDs

class TesteSaidasDeDados(TestCase):
    def setUp(self):
        """
        Gerando dataframes fictícios para testar as funções desaídas de dados para o usuário
        """
        # Nomes das colunas nos dataframes fictícios
        cols = ['data','cota','pl','cdi_dia','racumulado','rdiario','cdi_acumulado']
        # Objeto com os dados fictícios da data imediatamente anterior
        self.d0_fixo = pd.DataFrame([('2018-12-31',3.1988603600,128606230.3600000000,0.0002463300,0.0002463300,0.0002463300,0.0002463300)], columns=cols)
        # Construção de um dataframe fictício para testes
        data =  [('2019-01-02',3.2435904100,132288763.9300000000,0.0002462700,0.0002463300,0.0002463300,0.0002463300),
                ('2019-01-03',3.2487529000,135732753.6100000000,0.0002462100,0.0002463300,0.0002463300,0.0002463300),
                ('2019-01-04',3.2408214900,137455063.1000000000,0.0002461400,0.0002463300,0.0002463300,0.0002463300),
                ('2019-01-07',3.2098529400,139571749.0100000000,0.0002460800,0.0002463300,0.0002463300,0.0002463300),
                ('2019-01-08',3.2137812900,142517890.6200000000,0.0002460200,0.0002463300,0.0002463300,0.0002463300),
                ('2019-01-09',3.2240108900,146589692.8900000000,0.0002463000,0.0002463300,0.0002463300,0.0002463300),
                ('2019-01-10',3.2117679600,148146863.2800000000,0.0002462400,0.0002463300,0.0002463300,0.0002463300),
                ('2019-01-11',3.2110677200,150291110.4500000000,0.0002461800,0.0002463300,0.0002463300,0.0002463300)]

        self.df_fixo = pd.DataFrame(data, columns=cols) # dataframe do período

    def teste_geracao_das_strings_para_imprimir_resultado(self):
        """
        Teste para verificar se foi gerada a quantidade correta de strings a partir da função
        generate_strings com as informações que serão fornecidas ao usuário
        """
        quantidade_strings = 10 # Quantidade correta de strings a serem geradas
        self.assertEqual(len(generate_strings(self.d0_fixo,self.df_fixo)),quantidade_strings)

    def teste_impressao_de_resultados_na_tela(self):
        """
        Testando a impressão das informações de resultados contidas nas strings
        na tela do terminal para o usuário
        """
        self.assertTrue(print_results(self.d0_fixo,self.df_fixo))

    def teste_impressao_da_tabela_de_resultados_no_formato_esperado(self):
        """
        Testando a impressão da tabela de retorno diário do fundo no formato 'github' do pacote
        tabulate
        """
        padrao = r'(?:^[|].+|.+|$)' # Padrão esperado para a tabela
        texto = pprint_df(self.df_fixo) # Tabela gerada na função
        self.assertRegex(texto,padrao) # Validação do resultado utilizando Regex

    def teste_geracao_do_grafico_html(self):
        """
        Testando a geração do gráfico HTML contendo os retornos acumulados do fundo e do CDI e o
        retorno diário do fundo
        """
        filename = "retorno_teste.html" # Nome do arquivo html gerado pelo gráfico
        grafico_retorno(self.df_fixo,filename) # Geração do gráfico
        # Verificação se o arquivo existe
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