"""
@autor: Gabriel Marcos Magalhães
Arquivo onde estão escritas as funções relacionadas a manipulação dos dataframes
utilizados no programa
"""
import pandas as pd # Importação da biblioteca pandas (manipulação de dataframes)

def treat_df(df_full,intervalo):
    """
    Função responsável por realizar o tratamento do banco de dados inicial completo,
    obtendo um banco de dados apenas do período selecionado e inserindo novas colunas
    para retorno acumulado do fundo, retorno diário do fundo e retorno do CDI acumulado.

    Argumentos: df_full: Data frame completo extraído dos arquivos de entrada (dataframe pandas)
                intervalo: String com a data inicial [0] e a data final [1] do período
                            fornecido para análise (string).
    Retorno:d0: objeto contendo as informações iniciais da primeira data anterior 
                ao período fornecido (objeto)
            df: dataframe do período selecionado já contendo as informações calculadas
                (retorno acumulado do fundo, retorno diário do fundo e retorno do CDI acumulado)
    """
    # Indice da primeira data anterior ao período fornecido
    idx_data0 = df_full[(df_full.data < intervalo[0])].reset_index()['index'].iloc[-1]

    # Informações na primeira data anterior ao período fornecido
    d0 = df_full.loc[idx_data0]

    # Data frame contendo apenas os dados do período selecionado
    df = cortar_banco_de_dados(df_full,intervalo)

    # Inclusão do retorno acumulado do fundo no data frame
    df['racumulado'] = retorno_acumulado(d0.cota,df.cota)
    # Inclusão do retorno diário do fundo no data frame
    df['rdiario'] = retorno_diario(d0.cota,df.cota)
    # Inclusão do retorno acumulado do CDI no data frame
    df['cdi_acumulado'] = cdi_acumulado(df.cdi_dia)

    return(d0,df)

def cortar_banco_de_dados(df_full,intervalo):
    """
    Função responsável por realizar o tratamento do banco de dados inicial completo,
    obtendo um banco de dados apenas do período selecionado e inserindo novas colunas
    para retorno acumulado do fundo, retorno diário do fundo e retorno do CDI acumulado.

    Argumentos: df_full: Data frame completo extraído dos arquivos de entrada (dataframe pandas)
                intervalo: String com a data inicial [0] e a data final [1] do período
                            fornecido para análise (string).
    Retorno: df: dataframe do período selecionado contendo todas as informações de df_full
    """
    df = df_full[(df_full.data >= intervalo[0]) & (df_full.data <= intervalo[1])].reset_index(drop=True)
    return(df)


def retorno_acumulado(cota0,cotas):
    """
    Função responsável por calcular o retorno acumulado do fundo.

    Argumentos: cota0: Cota na primeira data anterior ao período fornecido
                cotas: Cota diária no período (série pandas)
    Retorno: rac: Retorno acumulado no período
    """
    rac = cotas.apply(lambda cota: (cota-cota0)/cota0)
    return(rac)

def retorno_diario(cota0,cotas):
    """
    Função responsável por calcular o retorno diário do fundo.

    Argumentos: cota0: Cota na primeira data anterior ao período fornecido
                cotas: Cota diária no período (série pandas)
    Retorno: rday: Retorno diário do fundo no período (série pandas)
    """
    rday = cotas.diff()/cotas.shift(1)
    rday.iloc[0] = (cotas.iloc[0]-cota0)/cota0

    return(rday)

def cdi_acumulado(cdi_dia):
    """
    Função responsável por calcular o retorno acumulado do CDI, partindo de 0.

    Argumentos: cdi_dia: Variação diária do CDI no período (série pandas)
    Retorno: cdi_ac: CDI acumulado diário no período (série pandas)
    """
    cdi_ac = (1 + cdi_dia).cumprod() - 1
    cdi_ac.iloc[0]=0

    return(cdi_ac)

