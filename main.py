import tkinter as tk
from tkinter import ttk
import pandas as pd
import locale
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Substitua 'nome-do-arquivo.xlsx' pelo nome do seu arquivo Excel
nome_arquivo = 'FINBRA_Estados-DF_Despesas_por_Função_2018-2021.xlsx'

# Carrega o arquivo Excel em um DataFrame do pandas
df = pd.read_excel(nome_arquivo, skiprows=4)

colunas_desejadas = ['Ano', 'UF', 'Coluna', 'Conta', 'Valor (R$)']

df_col_selecionadas = df[colunas_desejadas]

ld = ['08 - Assistência Social','09 - Previdência Social', '10 - Saúde']  # Deixar separado porque é o total das subfunções

linhas_desejadas = ['08.241 - Assistência ao Idoso',
                    '08.242 - Assistência ao Portador de Deficiência',
                    '08.243 - Assistência à Criança e ao Adolescente',
                    '08.244 - Assistência Comunitária',
                    '08.122 - Administração Geral',
                    'FU08 - Demais Subfunções',
                    '09.271 - Previdência Básica',
                    '09.272 - Previdência do Regime Estatutário',
                    '09.273 - Previdência Complementar',
                    '09.274 - Previdência Especial',
                    '09.122 - Administração Geral',
                    'FU09 - Demais Subfunções',
                    '10.301 - Atenção Básica',
                    '10.302 - Assistência Hospitalar e Ambulatorial',
                    '10.303 - Suporte Profilático e Terapêutico',
                    '10.304 - Vigilância Sanitária',
                    '10.305 - Vigilância Epidemiológica',
                    '10.306 - Alimentação e Nutrição',
                    '10.122 - Administração Geral',
                    'FU10 - Demais Subfunções']

lin_col_selecionadas = df_col_selecionadas['Conta'].isin(linhas_desejadas)

df_selecionado = df_col_selecionadas[lin_col_selecionadas]

# Exibe o conteúdo do DataFrame
# print(df.head())

def populate_table():
    global df_selecionado

    # Limpar a tabela existente
    for item in tree.get_children():
        tree.delete(item)

    # Obter os valores dos filtros dos campos de entrada
    selected_column = 'Ano'
    selected_option = option_combobox.get()

    selected_column2 = 'UF'
    selected_option2 = option_combobox2.get()

    # Filtrar os dados com base nos valores inseridos pelo usuário
    if selected_option != '' and selected_option2 != '':
        filtered_df = df_selecionado[
            (df_selecionado[selected_column].astype(str).str.contains(selected_option, case=False)) &
            (df_selecionado[selected_column2].astype(str).str.contains(selected_option2, case=False))
            ]
    elif selected_option != '' and selected_option2 == '':
        filtered_df = df_selecionado[df_selecionado[selected_column].astype(str).str.contains(selected_option, case=False)]

    elif selected_option2 != '' and selected_option == '':
        filtered_df = df_selecionado[df_selecionado[selected_column2].astype(str).str.contains(selected_option2, case=False)]
    else:
        filtered_df = df_selecionado

    # Preencher a tabela com os dados filtrados
    for index, row in filtered_df.iterrows():
        tree.insert("", "end", values=row.tolist())

    # Obtém o nome da coluna do Entry
    coluna = 'Valor (R$)'

    # Calcula o total da coluna
    total_gasto = filtered_df[coluna].sum()

    total_formatado = locale.currency(total_gasto, grouping=True)

    # Total por Função
    lin_assist_soc = filtered_df['Conta'].isin(['08.241 - Assistência ao Idoso',
                                                   '08.242 - Assistência ao Portador de Deficiência',
                                                   '08.243 - Assistência à Criança e ao Adolescente',
                                                   '08.244 - Assistência Comunitária',
                                                   '08.122 - Administração Geral',
                                                   'FU08 - Demais Subfunções'])
    lin_col_assist_soc = filtered_df[lin_assist_soc]
    total_assist_soc = lin_col_assist_soc[coluna].sum()
    total_assist_soc_format = locale.currency(total_assist_soc, grouping=True)
    lin_prev_soc = filtered_df['Conta'].isin(['09.271 - Previdência Básica',
                                              '09.272 - Previdência do Regime Estatutário',
                                              '09.273 - Previdência Complementar',
                                              '09.274 - Previdência Especial',
                                              '09.122 - Administração Geral',
                                              'FU09 - Demais Subfunções'])
    lin_col_prev_soc = filtered_df[lin_prev_soc]
    total_prev_soc = lin_col_prev_soc[coluna].sum()
    total_prev_soc_format = locale.currency(total_prev_soc, grouping=True)
    lin_saude = filtered_df['Conta'].isin(['10.301 - Atenção Básica',
                                           '10.302 - Assistência Hospitalar e Ambulatorial',
                                           '10.303 - Suporte Profilático e Terapêutico',
                                           '10.304 - Vigilância Sanitária',
                                           '10.305 - Vigilância Epidemiológica',
                                           '10.306 - Alimentação e Nutrição',
                                           '10.122 - Administração Geral',
                                           'FU10 - Demais Subfunções'])
    lin_col_saude = filtered_df[lin_saude]
    total_saude = lin_col_saude[coluna].sum()
    total_saude_format = locale.currency(total_saude, grouping=True)

    # Exibe o resultado na Label
    if selected_option != '' and selected_option2 != '':
        resultado_label.config(text=f"Total Gasto com Seguridade Social do Governo do Estado do {selected_option2}, "
                                    f"no ano de {selected_option}: {total_formatado} \n "
                                    f"\n Assistência Social: {total_assist_soc_format} \n"
                                    f"\n Previdência Social: {total_prev_soc_format} \n"
                                    f"\n Saúde: {total_saude_format}", justify='left')

    elif selected_option == '' and selected_option2 != '':
        resultado_label.config(text=f"Total Gasto com Seguridade Social do Governo do Estado do {selected_option2}, "
                                    f"no período de 2018-2021: {total_formatado} \n"
                                    f"\n Assistência Social: {total_assist_soc_format} \n"
                                    f"\n Previdência Social: {total_prev_soc_format} \n"
                                    f"\n Saúde: {total_saude_format}", justify='left')
    elif selected_option != '' and selected_option2 == '':
        resultado_label.config(text=f"Total Gasto com Seguridade Social de todos os Governos do Estado do Brasil, "
                                    f"no ano de {selected_option}: {total_formatado} \n"
                                    f"\n Assistência Social: {total_assist_soc_format} \n"
                                    f"\n Previdência Social: {total_prev_soc_format} \n"
                                    f"\n Saúde: {total_saude_format}", justify='left')
    else:
        resultado_label.config(text=f"Total Gasto com Seguridade Social de todos os Governos do Estado do Brasil,"
                                    f" no período de 2018-2021: {total_formatado} \n"
                                    f"\n Assistência Social: {total_assist_soc_format} \n"
                                    f"\n Previdência Social: {total_prev_soc_format} \n"
                                    f"\n Saúde: {total_saude_format}", justify='left')


def exibir_graficos():
    # Cria uma figura com dois subplots (gráficos)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    # Gráfico 1
    labels1 = ['Maçãs', 'Bananas', 'Uvas', 'Laranjas']
    sizes1 = [30, 25, 20, 25]
    cores1 = ['yellow', 'lightgreen', 'lightcoral', 'lightskyblue']
    ax1.pie(sizes1, labels=labels1, colors=cores1, autopct='%1.1f%%', startangle=140)
    ax1.set_title("Gráfico 1")

    # Gráfico 2
    labels2 = ['A', 'B', 'C', 'D']
    valores2 = [10, 20, 30, 40]
    cores2 = ['skyblue', 'lightcoral', 'lightgreen', 'lightpink']
    ax2.bar(labels2, valores2, color=cores2)
    ax2.set_title("Gráfico 2")

    # Cria um widget Canvas do Matplotlib
    canvas = FigureCanvasTkAgg(fig, master=aba2)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()


root = tk.Tk()
root.title("Programa de Análise Contábil - Seguridade Social FINBRA (2018-2021)")

# Defina o tamanho da janela
root.geometry("1050x600")
root.resizable(width=True, height=True)  # A janela é redimensionável tanto na largura quanto na altura

# --------------------------------------------------------
notebook = ttk.Notebook(root)

aba1 = ttk.Frame(notebook)
aba2 = ttk.Frame(notebook)

notebook.add(aba1, text="Seguridade Social por Estado e Ano")
notebook.add(aba2, text="Aba 2")
# -------------------------------------------------------

# Criar campo de seleção para escolher a coluna
# column_label = tk.Label(aba1, text="Selecione uma coluna:")
# column_label.pack()

# column_combobox = ttk.Combobox(aba1, values=["Ano"])
# column_combobox.pack()

# Criar campo de seleção para escolher uma opção
option_label = tk.Label(aba1, text="Selecione o Ano:", font=('Arial', 10))
option_label.pack()

option_combobox = ttk.Combobox(aba1, values=["2018", "2019", "2020", "2021"])
option_combobox.pack()

# ------------------------------------------------------------------

# Criar campo de seleção para escolher a outra coluna
# column_label2 = tk.Label(aba1, text="Selecione outra coluna:")
# column_label2.pack()

# column_combobox2 = ttk.Combobox(aba1, values=["UF"])
# column_combobox2.pack()

# Criar campo de seleção para escolher uma opção
option_label2 = tk.Label(aba1, text="Selecione o Estado:", font=('Arial', 10))
option_label2.pack()

option_combobox2 = ttk.Combobox(aba1, values=["AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS",
                                              "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC",
                                              "SE", "SP", "TO"])
option_combobox2.pack()

# Adiciona um espaço vertical de 20 pixels
espaco_vertical = tk.Frame(aba1, height=10)
espaco_vertical.pack()

# Criar a árvore (tabela)
tree = ttk.Treeview(aba1, columns=("Ano", "UF", "Coluna", 'Conta', 'Valor (R$)'), show="headings")
tree.heading("Ano", text="Ano")
tree.heading("UF", text="UF")
tree.heading("Coluna", text="Coluna")
tree.heading("Conta", text="Conta")
tree.heading("Valor (R$)", text="Valor (R$)")
tree.pack()

# Botão para preencher a tabela a partir do Excel
populate_button = tk.Button(aba1, text="Preencher Tabela", font=('Arial', 10), command=populate_table)
populate_button.pack()

# Adiciona um espaço vertical de 20 pixels
espaco_vertical = tk.Frame(aba1, height=10)
espaco_vertical.pack()

# ----------------------------------------------

# Label para exibir o resultado
resultado_label = tk.Label(aba1, text="", font=('Arial', 10))
resultado_label.pack()
# ----------------------------------------------

# Crie um botão para exibir os gráficos
botao_exibir = tk.Button(aba2, text="Exibir Gráficos", command=exibir_graficos)
botao_exibir.pack()

# Empacote o widget Notebook na janela
notebook.pack(padx=10, pady=10, fill="both", expand=True)

# Iniciar o loop principal da interface
root.mainloop()
