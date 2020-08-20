"""
@autor: Gabriel Marcos Magalhães
Arquivo onde estão escritos os testes para as funções utilizadas no tratamento do
dataframe que estão contidas no arquivo src/tratamento.py
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
from tratamento import * # biblioteca criada para manipulação do banco de dados
import pandas as pd

class TesteTratamentoBD(TestCase):
    def setUp(self):
        """
        Gerando dataframes fictícios para testar as funções de manipulação de dataframes
        """
        # Nome das colunas nos dataframes fictícios
        cols = ['data','cota','pl','cdi_dia']
        # Dataframe com as informações na data base (d0)
        self.d0_fixo = pd.DataFrame([('2018-12-31',3.1988603600,128606230.3600000000,0.0002463300)], columns=cols)
        
        data =  [('2019-01-02',3.2435904100,132288763.9300000000,0.0002462700),
                ('2019-01-03',3.2487529000,135732753.6100000000,0.0002462100),
                ('2019-01-04',3.2408214900,137455063.1000000000,0.0002461400),
                ('2019-01-07',3.2098529400,139571749.0100000000,0.0002460800),
                ('2019-01-08',3.2137812900,142517890.6200000000,0.0002460200),
                ('2019-01-09',3.2240108900,146589692.8900000000,0.0002463000),
                ('2019-01-10',3.2117679600,148146863.2800000000,0.0002462400),
                ('2019-01-11',3.2110677200,150291110.4500000000,0.0002461800),
                ('2019-01-14',3.2274809400,152994778.8800000000,0.0002461200),
                ('2019-01-15',3.2141802100,154829243.4200000000,0.0002460600),
                ('2019-01-16',3.2117290600,156807324.1600000000,0.0002463300),
                ('2019-01-17',3.2214323600,158643961.7500000000,0.0002462700),
                ('2019-01-18',3.2179236300,161457562.5800000000,0.0002462100),
                ('2019-01-21',3.2152717000,162787779.7300000000,0.0002461500),
                ('2019-01-22',3.2149908700,164700839.4200000000,0.0002460900),
                ('2019-01-23',3.2309630000,167535367.8800000000,0.0002460300),
                ('2019-01-24',3.2397354900,170147405.7300000000,0.0002463100),
                ('2019-01-25',3.2381515500,169981907.2600000000,0.0002462500),
                ('2019-01-28',3.2276130800,171812626.0500000000,0.0002461800),
                ('2019-01-29',3.2409437400,174418394.3200000000,0.0002461200),
                ('2019-01-30',3.2432877700,176975311.8600000000,0.0002460600),
                ('2019-01-31',3.2801294200,181434502.4600000000,0.0002463400)]
        # Dataframe com as informações de um dado periodo
        self.df_fixo = pd.DataFrame(data, columns=cols)

    def teste_cortando_banco_de_dados(self):
        """
        Testando o corte de um dataframe para gerar um novo dataframe contendo apenas
        informações do período de datas escolhido
        """
        # Geração de um novo dataframe com informações entre '2019-01-07' e '2019-01-11'
        saida = cortar_banco_de_dados(self.df_fixo,['2019-01-07','2019-01-11'])
        # Resultado esperado
        resultado = self.df_fixo[3:8].reset_index(drop=True)
        # Verificação se todos os elementos são iguais
        for column in saida:
            dfs_iguais = saida[column].all() == resultado[column].all()
        self.assertTrue(dfs_iguais)

    def teste_retorno_fundo_acumulado(self):
        """
        Testando o valor do retorno acumulado do fundo usando as informações de
        validação fornecidas
        """
        # Pega o retorno acumulado do último dia do período
        saida = retorno_acumulado(self.d0_fixo.cota,self.df_fixo.cota).iloc[-1,0]
        saida = round(saida,6) # Arredonda para o numero de casas decimais conhecidas
        resultado = 0.025406
        self.assertEqual(saida,resultado)

    def teste_retorno_cdi_acumulado(self):
        """
        Testando o valor do retorno acumulado do CDI usando as informações de
        validação fornecidas
        """
        # Pega o retorno acumulado do último dia do período
        saida = cdi_acumulado(self.df_fixo.cdi_dia)
        saida = round(saida.iloc[-1],6) # Arredonda para 6 casas decimais
        resultado = round(0.025406/(467.8768/100.0),6) # Resultado baseado nos dados de validação
        self.assertEqual(saida,resultado)

    def teste_retorno_diario_maximo_e_minimo_valor_e_data(self):
        """
        Testando o valor e data dos retornos diários máximo e mínimo do fundo usando as informações de
        validação fornecidas
        """
        saida = retorno_diario(self.d0_fixo.cota.values,self.df_fixo.cota)
        #Teste valor retorno diário máximo
        with self.subTest(saida=saida):
            retorno = saida.max() # Calcula o retorno maximo
            retorno = round(retorno,6) # Arredonda para o numero de casas decimais conhecidas
            resultado = 0.013983
            self.assertEqual(retorno,resultado,msg="Falhou ao encontrar o valor do retorno máximo")
        #Teste data retorno diário máximo
        with self.subTest(saida=saida):
            idx_retorno = saida.idxmax() # Calcula o retorno maximo
            data_retorno = self.df_fixo.data.iloc[idx_retorno] # Arredonda para o numero de casas decimais conhecidas
            resultado = '2019-01-02'
            self.assertEqual(data_retorno,resultado,msg="Falhou ao encontrar a data do retorno máximo")
        #Teste valor retorno diário minimo
        with self.subTest(saida=saida):
            retorno = saida.min() # Calcula o retorno maximo
            retorno = round(retorno,6) # Arredonda para o numero de casas decimais conhecidas
            resultado = -0.009556
            self.assertEqual(retorno,resultado,msg="Falhou ao encontrar o valor do retorno minimo")
        #Teste data retorno diário máximo
        with self.subTest(saida=saida):
            idx_retorno = saida.idxmin() # Calcula o retorno maximo
            data_retorno = self.df_fixo.data.iloc[idx_retorno] # Arredonda para o numero de casas decimais conhecidas
            resultado = '2019-01-07'
            self.assertEqual(data_retorno,resultado,msg="Falhou ao encontrar a data do retorno minimo")

if __name__ == '__main__':
    main()