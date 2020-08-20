"""
@autor: Gabriel Marcos Magalhães
Arquivo onde estão escritas as funções relacionadas a manipulação de datas
utilizados no programa
"""
import pandas as pd # Importação da biblioteca pandas (manipulação de dataframes)
import re # Biblioteca para uso de RegEx
from datetime import datetime # Biblioteca para formatação da data

def le_data(min_data,max_data):
    """
    Função responsável pela leitura e validação das datas fornecidas pelo usuário e validação do intervalo
    de datas fornecido.

    Argumentos: min_data: mínima data contida no banco de dados
                max_data: máxima data contida no banco de dados
    Retorno: lista com as (strings) das datas de início e final do intervalo, respectivamente, no formato 
            AAAA-MM-DD se as datas forem válidas ou False se a data for inválida
    """
    print(f'O banco de dados atual vai de {pdata(min_data)} a {pdata(max_data)} \n\n')
    # Leitura e validação da a data de INICIO do período
    data1 = input("\n Insira a data de INÍCIO no formato DD/MM/AAAA: ")
    # data1 = '02/01/2019'
    data1_fmt = valida_data(data1)
    if (not data1_fmt):
        print("Data inválida")
        return False

    # Leitura e validação da a data de FINAL do período
    data2 = input("\n Insira a data de FINAL no formato DD/MM/AAAA: ")
    # data2 = '31/01/2019'
    data2_fmt = valida_data(data2)
    if (not data2_fmt):
        print("Data inválida")
        return False

    # Validação do intervalo fornecido
    if valida_intervalo(min_data,max_data,data1_fmt,data2_fmt):
        print(f'\n\n\n O intervalo selecionado para análise começa em {data1} e termina em {data2} \n\n\n')
        return([str(data1_fmt),str(data2_fmt)])
    else:
        print("\n\n\n O intervalo fornecido é inválido. Por favor forneça um intervalo de datas válido \n\n\n")
        return False

def valida_data(data):
    """
    Função responsável pela validação de uma data fornecida usando as bibliotecas datetime e RegEx e 
    retornar a data no formato do banco de dados.

    Argumentos: data: data no formato DD/MM/AAAA
    Retorno: data_fmt: data no formato AAAA-MM-DD se a data for válida ou False se a data for inválida
    """
    # Verificando se a data atende ao formato desejado
    padrao = r"(?P<dia>^\d{2})/(?P<mes>\d{2})/(?P<ano>\d{4}$)"
    aux = re.search(padrao,data)
    # Se a data atende ao padrão
    if(aux):
        try:
            # Formatação da data para AAAA-MM-DD
            data_fmt = datetime(int(aux.group('ano')),int(aux.group('mes')),int(aux.group('dia'))).date()
            return data_fmt
        except ValueError:
            return False
    else:
        return False

def valida_intervalo(min_data,max_data,data_ini,data_fim):
    """
    Função responsável pela validação do intervalo de dados fornecido. Verifica se:
        - A data inicial está contida no banco de dados
        - A data final está contida no banco de dados
        - A data final é maior que a data inicial
        - A data final é igual a data inicial 
    Argumentos: min_data: mínima data contida no banco de dados
                max_data: máxima data contida no banco de dados
                data_ini: data de INÍCIO do período
                data_fim: data de FINAL do período
    Retorno: True se a data for válida, False se não for
    """
    # Formatação das datas mínima e máxima do banco de dados
    min_data = datetime.strptime(min_data, '%Y-%m-%d').date()
    max_data = datetime.strptime(max_data, '%Y-%m-%d').date()
    # Verificação de validade do intervalo
    if((data_ini < min_data) or (data_fim > max_data) or (data_fim < data_ini) or (data_fim == data_ini)):
        return False
    else:
        return True

def pdata(data):
    """
    Função responsável pela conversão de uma data (string) no formato AAAA-MM-DD para DD/MM/AAAA. Esta
    função é utilizada na exibição de dados para o usuário visando facilitar a compreensão. O nome é uma
    abreviação de pretty data.

    Argumentos: data: data no formato AAAA-MM-DD (string)
    Retorno: string com a data no formato DD/MM/AAAA se a data for válida ou False se o argumento for inválido
    """
    # Busca pelo padrão trabalhado usando grupos do RegEx
    padrao = r"(?P<ano>^\d{4})-(?P<mes>\d{2})-(?P<dia>\d{2}$)"
    aux = re.search(padrao,data)
    if aux:
        return(aux.group('dia')+"/"+aux.group('mes')+"/"+aux.group('ano'))
    else:
        return False