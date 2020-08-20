"""
@autor: Gabriel Marcos Magalhães
Arquivo onde estão escritas as funções relacionadas a construção de uma interface gráfica para
a aplicação em Python
"""
from tkinter import Pack, Tk, Frame, Label, IntVar, LEFT, RIGHT, Radiobutton, Button, Entry, messagebox, filedialog
# Bibliotecas desenvolvidas para o projeto
from data import valida_data, valida_intervalo, pdata # Manipulação de datas
from arquivo import le_arq # Leitura de arquivos
from saidas import print_relatorio, grafico_retorno # Saída de informações para o usuário
from tratamento import treat_df # Tratamento do dataframe

class Application:
    def __init__(self, master):
        """
        Função responsável pela inicialização
        """
        self.janela_principal = master
        self.fontePadrao = ("Arial", "11")
        self.fonteBotoes = ("Arial", "10")

    def interface(self):
        """
        Função responsável pela construção da interface 
        """
        self.define_titulo() # Definição do título interno da janela
        self.leitura_de_dados() # Leitura dos dados a partir de arquivos
        self.leitura_de_datas() # Leitura das datas do intervalo fornecido pelo usuário
        self.autenticar_datas() # Autenticação das datas e do intervalo fornecido pelo usuário
        self.botoes_finais() # Botões para operações finais

    def define_titulo(self):
        """
        Função responsável pela construção da parte relativa ao título na interface
        """
        # Construção do container para título da janela
        self.primeiroContainer = Frame(self.janela_principal)
        self.primeiroContainer["pady"] = 20
        self.primeiroContainer.pack()
        # Atribuição do título dentro da janela (1a informação exibida)
        self.titulo = Label(self.primeiroContainer, text="Dados do usuário")
        self.titulo["font"] = self.fontePadrao
        self.titulo.pack()

    def leitura_de_dados(self):
        """
        Função responsável pela construção da parte da interface relativa a leitura de
        dados dos arquivos CSV ou Excel
        """
        # Construção do container para a seleção da fonte dos dados
        self.arqContainer = Frame(self.janela_principal)
        self.arqContainer["padx"] = 80
        self.arqContainer["pady"] = 5
        self.arqContainer.pack()
        # Construção do container para exibir a informação a respeito dos dados lidos
        self.infoContainer = Frame(self.janela_principal)
        self.infoContainer["padx"] = 10
        self.infoContainer["pady"] = 5
        self.infoContainer.pack()

        # Informação sobre o que será escolhido
        self.box1Label = Label(self.arqContainer,text="Arquivo fonte dos dados: ", font=self.fontePadrao)
        self.box1Label.pack(side=LEFT)
        
        self.v = IntVar() # Variável de armazenamento do tipo de arquivo a ser lido
        self.v.set(0)  # inicializa escolhendo 0 -> Excel
        # Lista das fontes possíveis de dados
        self.arq_dados = [
            ("Excel"),
            ("CSV")
        ]
        # Criação de um botão de seleção que permite apenas uma escolha por vez
        for val, arq_dados in enumerate(self.arq_dados):
            self.box1 = Radiobutton(self.arqContainer, 
                        text=arq_dados,
                        padx = 20, 
                        variable=self.v, 
                        value=val).pack(side=LEFT)

        # Declaração das variáveis de range de data do dataframe (serão exibidas na informação)
        self.data_min = None
        self.data_max = None

        # Botão para efetuar a leitura dos dados do tipo de arquivo escolhido
        self.bbox = Button(self.arqContainer)
        self.bbox["text"] = "Ler dados"
        self.bbox["font"] = self.fonteBotoes
        self.bbox["width"] = 12
        self.bbox["command"] = self.valid_arq # Chamada da função utilizada para validar o arquivo escolhido
        self.bbox.pack()
        # Informação do intervalo de datas presente no dataframe lido
        self.info = Label(self.infoContainer, text="", font=self.fontePadrao)
        self.info.pack()

    def leitura_de_datas(self):
        """
        Função responsável pela construção da parte relacionada a leitura das datas na interface
        """
        # Construção do container para a entrada da data inicial do intervalo desejado
        self.segundoContainer = Frame(self.janela_principal)
        self.segundoContainer["padx"] = 20
        self.segundoContainer["pady"] = 10
        self.segundoContainer.pack()
        # Construção do container para a entrada da data final do intervalo desejado
        self.terceiroContainer = Frame(self.janela_principal)
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer.pack()

        # Informação exibida ao lado do campo para entrada da data inicial
        self.data1Label = Label(self.segundoContainer,text="Data inicial (DD/MM/AAAA): ", font=self.fontePadrao).pack(side=LEFT)
        # Campo para entrada da data inicial
        self.data1 = Entry(self.segundoContainer)
        self.data1["width"] = 30
        self.data1["font"] = self.fontePadrao
        self.data1.pack(side=LEFT)
        # Informação exibida ao lado do campo para entrada da data final
        self.data2Label = Label(self.terceiroContainer, text="Data final (DD/MM/AAAA): ", font=self.fontePadrao).pack(side=LEFT)
        # Campo para entrada da data final
        self.data2 = Entry(self.terceiroContainer)
        self.data2["width"] = 30
        self.data2["font"] = self.fontePadrao
        self.data2.pack(side=LEFT)
        # Verificação de autenticação e/ou existência das datas (false antes de autenticar)
        self.datas_validas = False

    def autenticar_datas(self):
        """
        Função responsável pela construção da parte relacionada a autenticação das datas
        e do intervalo escolhido na interface
        """
        # Construção do container para o botão de autenticação das datas
        self.quartoContainer = Frame(self.janela_principal)
        self.quartoContainer["pady"] = 2
        self.quartoContainer.pack()
        # Construção do botão de autenticação das datas
        self.autenticar = Button(self.quartoContainer)
        self.autenticar["text"] = "Autenticar datas"
        self.autenticar["font"] = self.fonteBotoes
        self.autenticar["width"] = 12
        # Chamada da função utilizada para validar as datas e o intervalo escolhido
        self.autenticar["command"] = self.valid_dates
        self.autenticar.pack()
        # Exibição da mensagem relativa as datas e ao intervalo escolhido (valido ou inválido)
        self.mensagem = Label(self.quartoContainer, text="", font=self.fontePadrao)
        self.mensagem.pack()

    def botoes_finais(self):
        """
        Função responsável pela construção da parte relacionada aos botões finais na interface:
        - Geração de um relatório PDF
        - Geração de gráfico HTML com o retorno acumulado do fundo e do CDI e retorno diário do fundo
        - Encerramento da aplicação)
        """
        # Construção do container para os botões inferiores:
        self.ultimoContainer = Frame(self.janela_principal)
        self.ultimoContainer["pady"] = 2
        self.ultimoContainer.pack()

        # Construção do botão para geração de relatório
        self.relatorio = Button(self.ultimoContainer)
        self.relatorio["text"] = "Gerar Relatório"
        self.relatorio["font"] = self.fonteBotoes
        self.relatorio["width"] = 12
        # Chamada da função utilizada para geração do relatório PDF
        self.relatorio["command"] = self.gera_relatorio
        self.relatorio.pack(side=LEFT)
        # Construção do botão para geração do gráfico de retorno
        self.reset = Button(self.ultimoContainer)
        self.reset["text"] = "Gerar gráfico de retornos"
        self.reset["font"] = self.fonteBotoes
        self.reset["width"] = 20
        # Chamada da função utilizada para geração do gráfico de retorno HTML
        self.reset["command"] = self.gera_grafico
        self.reset.pack(side=LEFT)
        # Construção do botão para encerramento da interface
        self.encerrar = Button(self.ultimoContainer)
        self.encerrar["text"] = "Sair"
        self.encerrar["font"] = self.fonteBotoes
        self.encerrar["width"] = 12
        # Chamada da função utilizada para encerrar a janela da aplicação
        self.encerrar["command"] = self.janela_principal.quit
        self.encerrar.pack()

    def valid_arq(self):
        """
        Função utilizada para estruturar o processo de validação da fonte de dados escolhida
        """
        formato = ["xlsx","csv"] # Formatos relacionados a Excel e CSV, respectivamente
        arquivo = self.v.get() # Leitura da opção escolhida pelo usuário
        # Verificação se é uma opção válida
        if(arquivo == 0 or arquivo == 1):
            self.df_full = le_arq(formato[arquivo]) # Leitura e armazenamento do dataframe completo
            # Verificação de sucesso na leitura
            if(type(self.df_full) == bool):
                self.info["text"] = "Não foi possível abrir o arquivo do banco de dados"
            else:
                self.data_min = self.df_full.data.iloc[1] # Data mínima presente no banco de dados
                self.data_max = self.df_full.data.iloc[-1] # Data máxima presente no banco de dados
                # Construção da mensagem informando a data mínima e a data máxima possíveis na análise
                self.info["text"] = f"O banco de dados escolhido começa em {pdata(self.data_min)} e termina em {pdata(self.data_max)}"
        else:
            self.info["text"] = "Ocorreu um problema na escolha do arquivo."

    def valid_dates(self):
        """
        Função utilizada para estruturar o processo de validação das datas e do intervalo escolhido pelo usuário
        """
        # Verificação de autenticação e/ou existência das datas
        self.datas_validas = False
        # Verificação da existencia do dataframe com os dados disponíveis
        if(self.data_min != None and self.data_max != None):
            data1 = valida_data(self.data1.get()) # Validação da data inicial do usuário
            data2 = valida_data(self.data2.get()) # Validação da data final do usuário
            if(data1 and data2):
                intervalo_valido = valida_intervalo(self.data_min,self.data_max,data1,data2)
                if(intervalo_valido):
                    # Datas e intervalo válidos.
                    self.datas_validas = True # Datas e intervalo válidos
                    self.intervalo = [str(data1),str(data2)] # Definição do intervalo
                    self.tratamento_dados() # Adequação do dataframe ao período selecionado
                    # Mensagem com a informação do intervalo contido no banco de dados
                    self.mensagem["text"] = f"O intervalo selecionado para análise começa em {pdata(self.intervalo[0])} e termina em {pdata(self.intervalo[1])} (%d dias)"%((data2-data1).days)
                else:
                    # Mensagem para informar que o intervalo escolhido pelo usuário é inválido
                    self.mensagem["text"] = "As datas são válidas mas o intervalo é inválido"
            else:
                # Construção da mensagem informando quais datas fornecidas são inválidas
                s = "Data(s) inválida(s): "
                if(not data1):
                    s = s + "(Inicial) "
                if(not data2):
                    s = s + "(Final) "

                self.mensagem["text"] = s
        else:
            # Para validar o intervalo os dados precisam ser lidos para extração do máximo intervalo possível
            messagebox.showinfo('Status','O banco de dados deve ser lido antes de autenticar as datas.')

    def tratamento_dados(self):
        """
        Função utilizada para obtenção da data base (d0) e do dataframe baseados no intervalo selecionado pelo usuário (df)
        """
        [self.d0,self.df] = treat_df(self.df_full,self.intervalo)

    def gera_relatorio(self):
        """
        Função utilizada para geração de um relatório PDF
        """
        # Só constroi o relatório para datas e intervalos válidos
        if(not self.datas_validas):
            messagebox.showinfo('Status','Ocorreu um erro na geração do relatório')
            return False
        # Definição do nome e caminho do relatório gerado
        filename = ''
        filename =  filedialog.asksaveasfilename(initialdir = "./",title = "Select file",filetypes = (("pdf files","*.pdf"),("all files","*.*")))
        # Nome vazio -> Botão Cancel
        if (filename == '' or type(filename) is tuple):
            pass
        else:
            try:
                print_relatorio(self.d0,self.df,filename) # Geração do relatório PDF
                # Nova janela com mensagem de sucesso na operação
                messagebox.showinfo('Status',f'Relatório do período {pdata(self.intervalo[0])} a {pdata(self.intervalo[1])} gerado com sucesso')
            except:
                # Nova janela com mensagem de insucesso na operação
                messagebox.showinfo('Status','Ocorreu um erro na geração do relatório')


    # Método para gerar o relatório
    def gera_grafico(self):
        """
        Função utilizada para geração de um relatório PDF
        """
        # Só constroi o gráfico para datas e intervalos válidos
        if(not self.datas_validas):
            messagebox.showinfo('Status','Ocorreu um erro na geração do relatório')
            return False
        # Definição do nome e caminho do relatório gerado
        filename = ''
        filename =  filedialog.asksaveasfilename(initialdir = "./",title = "Select file",filetypes = (("html files","*.html"),("all files","*.*")))
        # Nome vazio -> Botão Cancel
        if (filename == '' or type(filename) is tuple):
            pass
        else:
            try:
                grafico_retorno(self.df,filename) # Geração do gráfico
                # Nova janela com mensagem de sucesso na operação
                messagebox.showinfo('Status',f'Gráfico do período {pdata(self.intervalo[0])} a {pdata(self.intervalo[1])} gerado com sucesso')
            except:
                # Nova janela com mensagem de insucesso na operação
                messagebox.showinfo('Status','Ocorreu um erro na geração do gráfico')

def main():
    """
    Função principal. Inicializa a aplicação e constrói a interface
    """
    root = Tk()
    root.title('Análise Zarathustra') # Título na barra superior da janela principal
    zaragui = Application(root) # Inicialização
    zaragui.interface() # Execução da interface
    root.mainloop()

if __name__ == "__main__":
    main()