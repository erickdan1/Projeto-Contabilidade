import tkinter as tk
from tkinter import ttk
import pandas as pd
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Substitua 'nome-do-arquivo.xlsx' pelo nome do seu arquivo Excel
nome_arquivo = 'FINBRA_Estados-DF_Despesas_por_Função_2018-2021.xlsx'

# Carrega o arquivo Excel em um DataFrame do pandas
df = pd.read_excel(nome_arquivo, skiprows=4)

colunas_desejadas = ['Ano', 'UF', 'Coluna', 'Conta', 'Valor (R$)']

df_col_selecionadas = df[colunas_desejadas]

linhas_desejadas = ['08 - Assistência Social',
                    '08.241 - Assistência ao Idoso',
                    '08.242 - Assistência ao Portador de Deficiência',
                    '08.243 - Assistência à Criança e ao Adolescente',
                    '08.244 - Assistência Comunitária',
                    '08.122 - Administração Geral',
                    'FU08 - Demais Subfunções',
                    '09 - Previdência Social',
                    '09.271 - Previdência Básica',
                    '09.272 - Previdência do Regime Estatutário',
                    '09.273 - Previdência Complementar',
                    '09.274 - Previdência Especial',
                    '09.122 - Administração Geral',
                    'FU09 - Demais Subfunções',
                    '10 - Saúde',
                    '10.301 - Atenção Básica',
                    '10.302 - Assistência Hospitalar e Ambulatorial',
                    '10.303 - Suporte Profilático e Terapêutico',
                    '10.304 - Vigilância Sanitária',
                    '10.305 - Vigilância Epidemiológica',
                    '10.306 - Alimentação e Nutrição',
                    '10.122 - Administração Geral',
                    'FU10 - Demais Subfunções',
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

    total = float(total_gasto)

    total_formatado = locale.currency(total, grouping=True)

    # Exibe o resultado na Label
    if selected_option != '' and selected_option2 != '':
        resultado_label.config(text=f"Total Gasto com Seguridade Social do Governo do Estado do {selected_option2}, no ano de {selected_option}: \n {total_formatado}")
    elif selected_option == '' and selected_option2 != '':
        resultado_label.config(text=f"Total Gasto com Seguridade Social do Governo do Estado do {selected_option2}, no período de 2018-2021: \n {total_formatado}")
    elif selected_option != '' and selected_option2 == '':
        resultado_label.config(text=f"Total Gasto com Seguridade Social de Todos os Governo do Estado do Brasil, no ano de {selected_option}: \n {total_formatado}")
    else:
        resultado_label.config(text=f"Total Gasto com Seguridade Social de Todos os Governo do Estado do Brasil, no período de 2018-2021: \n {total_formatado}")

root = tk.Tk()
root.title("Programa de Análise Contábil - Seguridade Social FINBRA (2018-2021)")

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
option_label = tk.Label(aba1, text="Selecione o Ano:")
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
option_label2 = tk.Label(aba1, text="Selecione o Estado:")
option_label2.pack()

option_combobox2 = ttk.Combobox(aba1, values=["AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS",
                                              "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC",
                                              "SE", "SP", "TO"])
option_combobox2.pack()

# Adiciona um espaço vertical de 20 pixels
espaco_vertical = tk.Frame(aba1, height=20)
espaco_vertical.pack()

# ----------------------------------------------
# Label para exibir o resultado
resultado_label = tk.Label(aba1, text="")
resultado_label.pack()
# ----------------------------------------------

# Adiciona um espaço vertical de 20 pixels
espaco_vertical = tk.Frame(aba1, height=20)
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
populate_button = tk.Button(aba1, text="Preencher Tabela", command=populate_table)
populate_button.pack()

# Empacote o widget Notebook na janela
notebook.pack(padx=10, pady=10, fill="both", expand=True)

# Iniciar o loop principal da interface
root.mainloop()
