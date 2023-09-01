import tkinter as tk
from tkinter import ttk
import pandas as pd

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

# Acessar colunas específicas e realizar operações
# ano = df['Ano']
# coluna2 = df['Instituição']
# coluna3 = df['Cod.IBGE']
# uf = df['UF']
# coluna5 = df['População']
# tipos_desp = df['Coluna']
# funcoes = df['Conta']
# coluna8 = df['Identificador da Conta']
# valor = df['Valor (R$)']

# Foco em Ano, UF, Coluna (Tipos de Despesas), Conta (Funções), Valor

# Exemplo de operação: imprimir valores da ano, uf, tipos_desp, funcoes e valor lado a lado
# for anos, estados, despesas, func, val in zip(ano, uf, tipos_desp, funcoes, valor):
#     print(f'{anos} | {estados} | {despesas}| {func}| {val}')

# Assistência Social e suas subfuções
# assist_soc = df[df['Conta'] == '08 - Assistência Social']  # Filtrar linhas com base em uma condição
# assist_soc1 = df[df['Conta'] == '08.241 - Assistência ao Idoso']
# assist_soc2 = df[df['Conta'] == '08.242 - Assistência ao Portador de Deficiência']
# assist_soc3 = df[df['Conta'] == '08.243 - Assistência à Criança e ao Adolescente']
# assist_soc4 = df[df['Conta'] == '08.244 - Assistência Comunitária']
# assist_soc5 = df[df['Conta'] == '08.122 - Administração Geral']

def populate_table():
    global df_selecionado

    # Limpar a tabela existente
    for item in tree.get_children():
        tree.delete(item)

    # Obter os valores dos filtros dos campos de entrada
    selected_column = column_combobox.get()
    selected_option = option_combobox.get()

    selected_column2 = column_combobox2.get()
    selected_option2 = option_combobox2.get()

    # Filtrar os dados com base nos valores inseridos pelo usuário
    if selected_column != '' and selected_option != '' and selected_column2 != '' and selected_option2 != '':
        filtered_df = df_selecionado[
            (df_selecionado[selected_column].astype(str).str.contains(selected_option, case=False)) &
            (df_selecionado[selected_column2].astype(str).str.contains(selected_option2, case=False))
            ]
    elif selected_column != '' and selected_option != '' and selected_column2 == '' and selected_option2 == '':
        filtered_df = df_selecionado[df_selecionado[selected_column].astype(str).str.contains(selected_option, case=False)]

    elif selected_column2 != '' and selected_option2 != '' and selected_column == '' and selected_option == '':
        filtered_df = df_selecionado[df_selecionado[selected_column2].astype(str).str.contains(selected_option2, case=False)]

    else:
        filtered_df = df_selecionado

    # Preencher a tabela com os dados filtrados
    for index, row in filtered_df.iterrows():
        tree.insert("", "end", values=row.tolist())


root = tk.Tk()
root.title("Tabela a partir de Banco de Dados do Excel")

# Criar campo de seleção para escolher a coluna
column_label = tk.Label(root, text="Selecione uma coluna:")
column_label.pack()

column_combobox = ttk.Combobox(root, values=["Ano"])
column_combobox.pack()

# Criar campo de seleção para escolher uma opção
option_label = tk.Label(root, text="Selecione sua linha:")
option_label.pack()

option_combobox = ttk.Combobox(root, values=["2018", "2019", "2020", "2021"])
option_combobox.pack()

# ------------------------------------------------------------------

# Criar campo de seleção para escolher a outra coluna
column_label2 = tk.Label(root, text="Selecione outra coluna:")
column_label2.pack()

column_combobox2 = ttk.Combobox(root, values=["UF"])
column_combobox2.pack()

# Criar campo de seleção para escolher uma opção
option_label2 = tk.Label(root, text="Selecione sua linha:")
option_label2.pack()

option_combobox2 = ttk.Combobox(root, values=["AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS",
                                              "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC",
                                              "SE", "SP", "TO"])
option_combobox2.pack()

# Criar a árvore (tabela)
tree = ttk.Treeview(root, columns=("Ano", "UF", "Coluna", 'Conta', 'Valor (R$)'), show="headings")
tree.heading("Ano", text="Ano")
tree.heading("UF", text="UF")
tree.heading("Coluna", text="Coluna")
tree.heading("Conta", text="Conta")
tree.heading("Valor (R$)", text="Valor (R$)")
tree.pack()

# Botão para preencher a tabela a partir do Excel
populate_button = tk.Button(root, text="Preencher Tabela", command=populate_table)
populate_button.pack()

# Iniciar o loop principal da interface
root.mainloop()
