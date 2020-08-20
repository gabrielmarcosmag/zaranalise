"""
@autor: Gabriel Marcos Magalhães
Arquivo onde estão escritas as funções relacionadas a geração de informações de saida
para o usuário
"""
import pandas as pd # Biblioteca pandas (manipulação de dataframes)
import locale # Biblioteca para formatação de milhares e decimais
from tabulate import tabulate # Biblioteca para formatação de tabelas para impressão
from escreve_pdf import relatorio # Função para escrever um relatório em PDF
from data import pdata # Função para reescrever uma data no formato DD/MM/AAAA
# Bibliotecas utilizadas para construção de gráficos com plotly
import plotly.offline as py
import plotly.graph_objs as go

def generate_strings(d0,df):
    """
    Função responsável por imprimir os resultados do período na tela para o usuário

    Argumentos  d0: Informações iniciais da primeira data anterior 
                    ao período fornecido (objeto)
                df: dataframe com as informações do período selecionado (dataframe pandas)
    Retorno: True se a operação for realizada com sucesso, False se não for
    """
    try:
        locale.setlocale(locale.LC_ALL, "") # Setup de locale utilizado para trocar , por . e . por ,
        s0 = "O relatório apresenta os indicadores para o período entre os dias %s e %s"%(pdata(df.data.iloc[0]),pdata(df.data.iloc[-1]))

        # (1) Rentabilidade do período
        rzara = df.racumulado.iloc[-1]
        s1 = f'(1) A rentabilidade do período em porcentagem foi de {locale.format("%1.4f",100*rzara,1)}%'

        #(2) Rentabilidade relativa ao CDI em porcentagem
        rcdi = df.cdi_acumulado.iloc[-1]
        s2 = f'(2) A rentabilidade do período relativa ao CDI foi de {locale.format("%1.4f",100*(rzara/rcdi),1)}%'

        # (3) Evolução do patrimônio do fundo em Reais (BRL)
        s3 = f'(3) A evolução do patrimônio do fundo em Reais (BRL) no período foi de R$ {locale.format("%1.2f",df.pl.iloc[-1] - d0.pl,1)}'

        # (4) Maior retorno diário e sua data de ocorrência
        rdia_max = df.rdiario.argmax()
        s4 = f'(4) O maior retorno diário foi de {locale.format("%1.4f",100*df.rdiario[rdia_max],1)}%, em {pdata(df.data[rdia_max])}'

        # (5) Menor retorno diário e sua data de ocorrência
        rdia_min = df.rdiario.argmin()
        s5 = f'(5) O menor retorno diário foi de {locale.format("%1.4f",100*df.rdiario[rdia_min],1)}%, em {pdata(df.data[rdia_min])}'

        # (6) Retorno diário médio do fundo
        s6 = "(6) O retorno diário médio do fundo no período foi de %s%%"%(locale.format("%1.4f",100*df['rdiario'].mean(),1))

        # (7) Retorno diário médio do CDI
        s7 = "(7) O retorno diário médio do CDI no período foi de %s%%"%(locale.format("%1.4f",100*df['cdi_dia'].mean(),1))

        # (8) Série de retorno acumulado do fundo
        s8 = "(8) Série de retorno acumulado do fundo: "
        s82 = pprint_df(df.loc[:,['data','racumulado']]) # Geração da tabela com o retorno acumulado em cada dia do período

        s = [s0,s1,s2,s3,s4,s5,s6,s7,s8,s82]

        return(s)
    except:
        print("Não foi possível gerar as strings")
        return False

def print_results(d0,df):
    """
    Função responsável por imprimir os resultados do período na tela para o usuário

    Argumentos  d0: Informações iniciais da primeira data anterior 
                    ao período fornecido (objeto)
                df: dataframe com as informações do período selecionado (dataframe pandas)
    Retorno: True se a operação for realizada com sucesso, False se não for
    """
    try:
        infos = generate_strings(d0,df) # Geração das strings com informações a serem escritas
        spc = "\n\n"
        print(spc)
        for info in infos:
            print(info+spc)
        return True
    except:
        print("Não foi possível imprimir os resultados")
        return False

def print_relatorio(d0,df,filename):
    """
    Função responsável por imprimir os resultados do período em um relatório PDF para o usuário

    Argumentos  d0: Informações iniciais da primeira data anterior 
                    ao período fornecido (objeto)
                df: dataframe com as informações do período selecionado (dataframe pandas)
    Retorno: True se a operação for realizada com sucesso, False se não for
    """
    try:
        info = generate_strings(d0,df) # Geração das strings com informações a serem escritas
        relatorio(info, filename) # Geração do relatório em PDF
        return True
    except:
        print("Não foi possível gerar o relatório")
        return False


def pprint_df(df):
    """
    Função responsável por formatar e imprimir na tela uma tabela a partir do dataframe
    fornecido

    Argumentos  df: dataframe com as informações a serem impressas
    Retorno: True se a operação for realizada com sucesso, False se não for
    """
    try:
        # Conversão das datas no formato AAAA-MM-DD para DD/MM/AAAA
        df.data = df['data'].apply(pdata)
        # Construção da tabela de retorno acumulado utilizando a biblioteca tabulate
        tabs = tabulate(df, headers=['Data', 'Retorno Acumulado'], tablefmt='github', showindex=False, floatfmt=".4%")
    except:
        return False
    return tabs.replace('.',',') # Retorna a tabela substituindo . por ,
    
def grafico_retorno(df,filename):
    """
    Função responsável por construir o gráfico de retornos acumulado do CDI e do fundo e do
    retorno diário do fundo

    Argumentos  df: dataframe com as informações a serem impressas
    Retorno: True se a operação for realizada com sucesso, False se não for
    """
    try:
        # Criando as estruturas de dados a serem plotadas

        # Retorno acumulado do CDI
        trace1 = go.Scatter(y = 100*df['cdi_acumulado'],
                            x = df['data'],
                            mode = 'lines',
                            name = 'CDI acumulado')
        # Retorno acumulado do Zarathustra
        trace2 = go.Scatter(y = 100*df['racumulado'],
                            x = df['data'],
                            mode = 'markers+lines',
                            name = 'Zarathustra acumulado')
        # Retorno diário do Zarathustra
        trace3 = go.Scatter(y = 100*df['rdiario'],
                            x = df['data'],
                            mode = 'markers+lines',
                            name = 'Zarathustra diário')

        # Dados que irão compor o gráfico
        data = [trace1,trace2,trace3]

        # Atributos da aparência do gráfico
        layout = go.Layout(title = f'Retornos no período entre {pdata(df.data[0])} e {pdata(df.data.iloc[-1])}',
                        titlefont = {'family': 'Arial',
                                        'size': 22,
                                        'color': '#7f7f7f'},
                        xaxis = dict(
                                title = "Data",
                                tickformat = '%d/%m/%Y',
                                range = [df.data[0],df.data.iloc[-1]]
                            ),
                        yaxis = {'title': 'Retorno (%)'}
                        )

        fig = go.Figure(data=data, layout=layout)

        plot = py.plot(fig, filename=filename)

        return True
    except:
        return False