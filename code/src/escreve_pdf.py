"""
@autor: Gabriel Marcos Magalhães
Arquivo onde estão escritas as funções relacionadas a escrita em um
documento PDF
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.rl_config import defaultPageSize
import re

def mm2p(milimetros):
    """
    Função para a conversão de um valor em mm para pt
    Argumento: milimetros: valor em mm (float)
    Retorno: valor convertido em pt (float)
    """
    return (milimetros/0.3527777778140355)

def relatorio(linhas,filename):
    """
    Função para escrever as strings contidas no argumento linhas em um
    documento PDF
    Argumentos: linhas: lista com as strings que devem ser escritas no PDF
                filename:  nome do arquivo PDF a ser gerado
                OBS: a última posição de linhas contém uma tabela, a qual é 
                submetida a um processo especial de escrita 
    Retorno: True se a operação for executada com sucesso e geração do arquivo
            filename PDF
    """
    PAGE_HEIGHT = defaultPageSize[1] # Definição da altura da página
    PAGE_WIDTH = defaultPageSize[0] # Definição da largura da página
    margem_y = mm2p(25.4) # Definição do valor da margem na direção Y (altura)
    cnv = canvas.Canvas(filename, pagesize=A4) # Atributos do arquivo a ser gerado
    gap = mm2p(8) # Espaço em mm entre as linhas
    inix = mm2p(10) # Posição inicial em X (largura), começando da margem esquerda
    iniy = PAGE_HEIGHT - margem_y # Posição inicial em Y (altura), começando da margem inferior
    cnv.setFont('Times-Bold',26) # Fonte do título do relatório
    cnv.drawString(inix,iniy,"Relatório de resultados") # Escrita do título do relatório
    posy = iniy - 2*gap
    cnv.setFont('Times-Roman',12) # Fonte de escrita das linhas
    cnv.drawString(inix,posy,linhas[0]) # Impressão da primeira linha
    posx = inix + gap
    posy -= gap
    # Impressão das demais linhas
    for i in range(1,len(linhas)-1):
        posy -= gap
        cnv.drawString(posx,posy,linhas[i])

    posy -= gap    
    # Identificação das linhas da tabela usando Regex (formato 'github' no pacote tabulate)
    tabela = re.findall(r'(?:^[|].+|.+|$)',linhas[-1])

    cnv.drawString(posx,posy,tabela[0]) # Título da tabela
    gap2 = mm2p(5) # Diminuição no espaçamento entre linhas para a tabela
    # Impressão dos dados contidos na tablea
    for i in tabela[2:]:
        if(posy < margem_y): # Análise de fim de página em Y
            cnv.showPage() # Geração de nova página
            posy = iniy # Reposicionamento na nova página
            cnv.drawString(posx,posy,tabela[0]) # Impressão do cabeçalho na nova página
        posy -= gap2
        cnv.drawString(posx,posy,i)

    cnv.save()
    return True
