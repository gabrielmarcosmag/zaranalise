"""
@autor: Gabriel Marcos Magalhães
Arquivo onde estão escritas as funções relacionadas a manipulação de arquivos de
entrada de dados utilizados no programa
"""
import pandas as pd # Importação da biblioteca pandas (manipulação de dataframes)
import re # Importação da biblioteca para trabalhar com Regex

def le_arq(formato):
    """
    Função responsável pela leitura de dados em um arquivo CSV e inserção em dois dataframes
    df_cdi (contendo os dados relativos ao CDI) e df_zara (contendo os dados relativos ao fundo)

    Argumentos: formato: formato do arquivo a ser lido (string)
    Retorno: dataframe pandas completo se a operação for realizada com sucesso, False se não for
            As colunas presentes no df_full são ['data', 'cota', 'pl', 'cdi_dia']
    """
    # Leitura do arquivo EXCEL
    if (formato == 'xlsx'):
        try:
            [df_zara,df_cdi] = le_excel("../dados/cotas_cdi_dados.xlsx")
        except:
            return False
    # Leitura do arquivo CSV
    elif(formato == 'csv'):
        try:
            [df_zara,df_cdi] = le_csv(["../dados/zarathustra.csv", "../dados/cdi.csv"])
        except:
            return False
    # Formato inválido fornecido
    else:
        print("Formato de arquivo inválido")
        return False

    # Criação de um único dataframe contendo os dados do fundo e a variação diária do CDI
    df_full = df_zara
    df_full['cdi_dia'] = df_cdi[df_cdi.columns[2]]

    return(df_full)

def le_csv(arq):
    """
    Função responsável pela leitura de dados em um arquivo CSV e inserção em dois dataframes
    df_cdi (contendo os dados relativos ao CDI) e df_zara (contendo os dados relativos ao fundo)

    Argumentos: arq: arquivo a ser lido (string)
    Retorno: dataframes pandas df_zara e df_cdi se a operação for realizada com sucesso, False se não for
    """
    # Verificação da existência dos arquivos fornecidos
    for i in range(len(arq)):
        if (not existencia_arquivo(arq[i])):
            print("O(s) arquivo(s) fornecido não existe(m) no diretório")
            return False
    try:
        # Extração dos dados dos arquivos CSV para os dataframes correspondentes
        df_zara = pd.read_csv(arq[0])
        df_cdi = pd.read_csv(arq[1])
        # Transformação da coluna de variação diária do CDI em porcentagem para valores absolutos
        df_cdi[df_cdi.columns[2]] = remove_porcentagem(df_cdi[df_cdi.columns[2]])

        return(df_zara, df_cdi)
    except:
        print("O arquivo fornecido apresenta problemas")
        return False

def le_excel(arq):
    """
    Função responsável pela leitura de dados em um arquivo EXCEL e inserção em dois dataframes
    df_cdi (contendo os dados relativos ao CDI) e df_zara (contendo os dados relativos ao fundo)

    Argumentos: arq: arquivo a ser lido (string)
    Retorno: dataframes pandas df_zara e df_cdi se a operação for realizada com sucesso, False se não for
    """
    # Verifica a existência do arquivo fornecido
    if (existencia_arquivo(arq)):
        try:
            # Lê os dados do arquivo  Excel fornecido
            arquivo_excel = pd.ExcelFile(arq)
            # Extrai os dados da aba Zarathustra para o dataframe df_zara
            df_zara = arquivo_excel.parse('Zarathustra')
            # Extrai os dados da aba CDI para o dataframe df_cdi
            df_cdi = arquivo_excel.parse('CDI')
            # Realiza a remoção da hora na coluda data do dataframe
            df_zara.data = remove_hora(df_zara.data)
            
            return(df_zara, df_cdi)
        except:
            print("O arquivo fornecido apresenta problemas")
            return False
    else:
        print("O(s) arquivo(s) fornecido não existe(m)")
        return False

def existencia_arquivo(arq):
    """
    Função responsável por verificar a existência de um arquivo fornecido

    Argumentos: arq: arquivo a ser lido (string)
    Retorno: True se a operação for realizada com sucesso, False se não for
    """
    try:
        with open(arq, 'r') as f:
            return True
    except FileNotFoundError as e:
        return False
    except IOError as e:
        return False

def remove_hora(data_df):
    """
    Função responsável por retirar a hora da coluna data. A hora acompanha a data
    quando o dataframe é obtido do arquivo excel

    Argumentos: data_df: série contendo as datas do dataframe (série pandas)
    Retorno: data sem a hora
    """
    data = pd.to_datetime(data_df)
    data = data.dt.strftime('%Y-%m-%d')
    return(data)


def remove_porcentagem(dados):
    """
    Função responsável por transformar uma coluna com dados em porcentagem em
    valores absolutos

    Argumentos: dados: série contendo os dados a serem modificados (série pandas)
    Retorno: série contendo os dados em valores absolutos (série pandas)
    """
    # Verifica padrão de número em porcentagem
    if(re.search(r'^\d+\.?\d*%$',dados.all())):
        dados = dados.replace(to_replace=r'%$', value='', regex=True)
        dados = dados.astype(float)/100.0
    return(dados)


