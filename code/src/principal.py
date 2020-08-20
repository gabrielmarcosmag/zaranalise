"""
@autor: Gabriel Marcos Magalhães
Função principal que faz a leitura do banco de dados dos aquivos, obtém um banco
de dados do período selecionado e imprime os resultados desejados
"""
import pandas as pd # Importação da biblioteca pandas (manipulação de dataframes)
import os
# Bibliotecas desenvolvidas para o projeto
from arquivo import le_arq # Leitura de arquivos
from data import le_data # Leitura de datas
from tratamento import treat_df # Tratamento do dataframe
from saidas import print_results, print_relatorio, grafico_retorno # Impressão dos resultados

def main():
    os.system("clear") # Limpeza do terminal

    # Escolha do formato do arquivo a ser usado (xlsx ou csv)
    formato = "xlsx"
    # Leitura do arquivo
    df_full = le_arq(formato)
    if(type(df_full) == bool): return False

    # Extração das datas mínima e máxima do banco de dados completo
    data_min = df_full.data.iloc[1] # Data mínima presente no banco de dados
    data_max = df_full.data.iloc[-1] # Data máxima presente no banco de dados

    # Definição do intervalo para análise dos dados
    intervalo = le_data(data_min,data_max)
    if (not intervalo):
        return False

    # Tratamento dos dados do dataframe original
    [d0,df] = treat_df(df_full,intervalo)

    # Impressão dos resultados
    try:
        print_results(d0,df)
        print_relatorio(d0,df,"relatorio.pdf")
        grafico_retorno(df,"retornos.html")
    except:
        print("Não foi possível imprimir os resultados")
        return False

if __name__ == "__main__":
    main()