# Análise de retorno do fundo Giant Zarathustra

O **Giant Zarathustra**, é um fundo de investimentos multimercado que conta com algumas estratégias quantitativas e é gerido pela **Giant Steps Capital**.

Baseado em um banco de dados contendo os retornos do fundo foi criada uma aplicação em Python que fornece ao usuário algumas informações relativas ao **Giant Zarathustra**.

Dado um range de datas, a aplicação fornece:
 1. **A rentabilidade do período em porcentagem;**
 2. **A rentabilidade relativa ao CDI em porcentagem;**
 3. **A evolução do patrimônio do fundo em Reais (BRL);**
 4. **A data e o valor de maior retorno diário em porcentagem;**
 5. **A data e o valor de menor retorno diário em porcentagem;**
 6. **O retorno diário médio do fundo;**
 7. **O retorno diário médio do CDI;**
 8. **Uma tabela com a série de retorno acumulado do fundo;**
 9. **Um gráfico do período contendo o retorno diário e o retorno acumulado do fundo e o retorno acumulado do CDI.**

Na aplicação desenvolvida existem três possibilidades:
 1. **Execução da aplicação utilizando o terminal para entrada e saída de dados;**
 2. **Execução da aplicação por meio de uma interface gráfica para entrada e saída de dados;**
 3. **Realização de testagem da aplicação desenvolvida.**

As possibilidades de execução e a divisão do código serão explicadas separadamente a seguir.
* **
## Preparação do ambiente

Existem duas opções para preparar o ambiente para a execução do código:

### 1 - Utilização do Docker
A utilização do Docker é indicada para desenvolvedores que não tenham a necessidade de visualizar a interface gráfica construída ou acessar os arquivos PDF e HTML gerados.
Para utilizar o Docker na preparação do ambiente, abra o terminal na pasta  `zaranalise`, onde está o documento `Dockerfile` e, para gerar a imagem, digite o comando:

    docker build -t nome_da_imagem .

a seguir, para rodar a imagem gerada, execute o comando:

    docker run -it nome_da_imagem

Será aberto um terminal na pasta `code` e a partir daí podem ser realizadas a **execução da aplicação utilizando o terminal para entrada e saída de dados** ou a **testagem da aplicação desenvolvida**

**IMPORTANTE:** Não é possível executar a opção de **execução da aplicação por meio de uma interface gráfica para entrada e saída de dados**. Portanto, para que se tenha acesso à interface gráfica bem como ao relatório PDF e o gráfico HTML é recomendada a opção pela instalação dos pacotes recomendados, explicada a seguir.

### 2 - Instalação dos pacotes necessários

A lista de pacotes necessários para a execução do programa é a seguinte:

 * pandas
 * xlrd
 * plotly
 * tabulate
 * reportlab
 * setuptools
 * python3-tk

Dos pacotes listados acima, apenas o *tk* não pode ser instalado via pip3. Portanto, o passo a passo para preparação do ambiente, partindo do princípio de que a máquina já possua o `python3` instalado seria:

 1. Execute o comando

        sudo apt updtate

 1. Instale o `pip3`, caso ainda não tenha instalado, utilizando o comando:

        sudo apt install python3-pip

 2. Instale o `python3-tk`, caso ainda não tenha instalado, utilizando o comando:

        sudo apt install python3-tk

 3. Instale o `setuptools`, caso ainda não tenha instalado, utilizando o comando:

        pip3 install setuptools

 4. Instale os demais pacotes usando o `pip3`. Para isso basta abrir um terminal na pasta `zaranalise`, onde está o arquivo `requirements.txt` e executar o comando

        pip3 install -r requirements.txt

Ao final do processo, a mensagem exibida, podendo haver variação na versão dos pacotes, será 

        Successfully installed numpy-1.19.1 pandas-1.1.0 pillow-7.2.0 plotly-4.9.0 python-dateutil-2.8.1 pytz-2020.1 reportlab-3.5.48 retrying-1.3.3 six-1.15.0 tabulate-0.8.7 xlrd-1.2.0

Caso nenhuma mensagem de erro apareça seu ambiente estará pronto para executar todas as funcionalidades da aplicação.

* **
## Possibilidades de execução

Todos os arquivos relacionados ao código estão armazenados na pasta `code`, portanto as instruções a seguir pressupõem que esta pasta já está sendo acessada via terminal ou interface gráfica do sistema operacional

### 1 - Execução da aplicação utilizando o terminal para entrada e saída de dados

Para executar a aplicação utilizando o terminal, basta abrir o terminal na pasta `src` e executar o seguinte comando:

    python3 principal.py

O programa começará a ser executado e apresentará, por exemplo, as seguintes informações na tela:

    O banco de dados atual vai de 08/03/2012 a 14/01/2020 

        Insira a data de INÍCIO no formato DD/MM/AAAA: 

inserindo uma data inválida será exibida a mensagem `Data inválida` e o programa será encerrado. Caso uma data válida de início seja inserida, a mensagem exibida será:

    Insira a data de FINAL no formato DD/MM/AAAA: 

inserindo uma data inválida será exibida a mensagem `Data inválida` e o programa será encerrado. Caso uma data válida de final seja inserida e o intervalo fornecido seja válido, a mensagem exibida será, por exemplo:

    O intervalo selecionado para análise começa em 02/05/2018 e termina em 02/08/2018

A seguir serão apresentados na tela do terminal todos os nove resultados listados no início deste documento.

Caso o intervalo inserido pelo usuário não seja válido, será exibida a seguinte mensagem na tela do terminal:

    O intervalo fornecido é inválido. Por favor forneça um intervalo de datas válido.

Ao fim da execução do programa, na pasta `src` são gerados um relatório no formato PDF com o nome `relatorio.pdf` contendo as informações listadas, exceto o gráfico. O gráfico contendo os retornos é gerado no arquivo `retornos.html`. Este gráfico já é aberto automaticamente no navegador e, nele é possível esconder qualquer uma das curvas clicando sobre o nome da curva que aparece ao lado direito do gráfico.


### 2 - Execução da aplicação por meio de uma interface gráfica para entrada e saída de dados

Para executar a aplicação utilizando o terminal, basta abrir o terminal na pasta `src` e executar o seguinte comando:

    python3 interface.py

O programa começará a ser executado e apresentará uma janela com a interface gráfica desenvolvida. O passo a passo que deve ser seguido é o seguinte:

 1. Escolher se os dados serão lidos do banco de dados em Excel ou csv, bastando marcar a opção de ler dados;
 2. Clicar no botão `Ler dados` para carregar o banco de dados;
 3. Será exibida, logo abaixo, uma informação sobre o intervalo de datas onde existem dados armazenados;
 4. Inserir a data inicial do intervalo para o qual se deseja obter as informações no campo *Data inicial*;
 5. Inserir a data final do intervalo para o qual se deseja obter as informações no campo *Data final*;
 6. Clicar no botão `Autenticar datas` para verificar se as datas e o intervalo são válidos. A mensagem informando a validade das datas e do intervalo será exibida logo abaixo do botão;
 7. Clicar no botão `Gerar Relatório` para gerar um relatório em PDF com as informações listadas no início deste documento. Ao clicar no botão será exibida uma janela para que se escolha o caminho e o nome do relatório gerado. Clicando em `Save` o relatório será salvo no destino escolhido e será exibida uma nova janela informando se o relatório foi gerado com êxito.
 8. Clicar no botão `Gerar gráfico de retornos` para gerar um gráfico HTML contendo os retornos. Ao clicar no botão será exibida uma janela para que se escolha o caminho e o nome do gráfico gerado. Clicando em `Save` o gráfico será salvo no destino escolhido e será exibida uma nova janela informando se o gráfico foi gerado com êxito e o mesmo será aberto automaticamente no navegador.
 9. Clicando no botão `Sair` a interface será encerrada.

**IMPORTANTE:** Caso as datas nos campos *Data inicial* e/ou *Data final* sejam modificadas deve-se pressionar novamente os botões `Gerar Relatório` e/ou `Gerar gráfico de retornos` para gerar os resultados relativos ao novo intervalo.

### 3 - Realização de testagem da aplicação desenvolvida

Para aplicar os testes desenvolvidos basta abrir o terminal na pasta `testes` e executar o seguinte comando:

    python3 -m unittest -b

Ao digitar esse comando será apresentado o seguinte resultado caso todos os testes sejam aplicados com sucesso

    ----------------------------------------------------------------------
    Ran 48 tests in x s

    OK

onde x é o tempo em segundos gasto na execução de todos os testes.

* **

## Divisão do código
Arquivo onde estão escritos os testes relacionados as funções responsáveis por saídas de dados
para o usuário que estão escritas no arquivo src/saidas.py
A pasta raiz contém três diretórios distintos:

 * **dados**: Diretório onde estão os arquivos `cotas_cdi_dados.xlsx`, `zarathustra.csv` e `cdi.csv`, onde são armazenados os dados utilizados pelo programa.

 * **src**: Diretório onde estão armazenados os arquivos Python relativos ao código fonte do programa desenvolvido.
    - [arquivo.py](./code/src/arquivo.py): Arquivo onde estão escritas as funções relacionadas a manipulação de arquivos de entrada de dados utilizados no programa;
    - [data.py](./code/src/data.py): Arquivo onde estão escritas as funções relacionadas a manipulação de datas
utilizados no programa;
    - [escreve_pdf.py](./code/src/escreve_pdf.py): Arquivo onde estão escritas as funções relacionadas a escrita em um documento PDF;
    - [interface.py](./code/src/interface.py): Arquivo onde estão escritas as funções relacionadas a construção de uma interface gráfica para a aplicação em Python
    - [principal.py](./code/src/principal.py): Programa principal que faz a leitura do banco de dados dos aquivos, obtém um banco de dados do período selecionado e imprime os resultados desejados.
    - [saidas.py](./code/src/saidas.py): Arquivo onde estão escritas as funções relacionadas a geração de informações de saida para o usuário.
    - [tratamento.py](./code/src/tratamento.py): Arquivo onde estão escritas as funções relacionadas a manipulação dos dataframes utilizados no programa


 * **testes**: Diretório onde estão armazenados os arquivos Python relativos aos testes do código fonte.
    - [testes_arquivo.py](./code/testes/testes_arquivo.py): Arquivo onde estão escritos os testes relacionados as funções responsáveis pela manipulação de arquivos de entrada de dados que estão escritas no arquivo [arquivo.py](code/src/arquivo.py)
    - [testes_data.py](./code/testes/testes_data.py): Arquivo onde estão escritos os testes relacionados as funções responsáveis pela manipulação de datas que estão escritas no arquivo [data.py](code/src/data.py)
    - [testes_escrevepdf.py](./code/testes/testes_escrevepdf.py): Arquivo onde estão escritos os testes relacionados as funções responsáveis por escrever um arquivo PDF com informações que estão escritas no arquivo [escreve_pdf.py](code/src/escreve_pdf.py)
    - [testes_saidas.py](./code/testes/testes_saidas.py): Arquivo onde estão escritos os testes relacionados as funções responsáveis por saídas de dados para o usuário que estão escritas no arquivo [saidas.py](code/src/saidas.py)
    - [testes_tratamento.py](./code/testes/testes_tratamento.py): Arquivo onde estão escritos os testes para as funções utilizadas no tratamento do dataframe que estão contidas no arquivo [tratamento.py](code/src/tratamento.py)

