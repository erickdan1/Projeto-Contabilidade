import tkinter as tk
from tkinter import ttk
import pandas as pd

# Substitua 'nome-do-arquivo.xlsx' pelo nome do seu arquivo Excel
nome_arquivo = 'FINBRA_Estados-DF_Despesas por Função_2018-2021.xlsx'

# Carrega o arquivo Excel em um DataFrame do pandas
df = pd.read_excel(nome_arquivo, skiprows=4)

# Exibe o conteúdo do DataFrame
# print(df.head())

# Acessar colunas específicas e realizar operações
coluna1 = df['Ano']
coluna2 = df['Instituição']
coluna3 = df['Cod.IBGE']
coluna4 = df['UF']
coluna5 = df['População']
coluna6 = df['Coluna']
coluna7 = df['Conta']
coluna8 = df['Identificador da Conta']
coluna9 = df['Valor (R$)']

# Foco em Ano, UF, Coluna (Tipos de Despesas), Conta (Funções), Valor

# Exemplo de operação: imprimir valores da coluna1 e coluna2 lado a lado
for valor1, valor4, valor6, valor7, valor9 in zip(coluna1, coluna4, coluna6, coluna7, coluna9):
    print(f'{valor1} | {valor4} | {valor6}| {valor7}| {valor9}')

linhas_filtradas = df[df['Nome da Coluna'] == 'Valor de Referência']  # Filtrar linhas com base em uma condição

def filtrar_dados():
    # Aqui você pode implementar a lógica de filtragem dos dados
    # Os valores dos campos de filtro podem ser obtidos com as variáveis filtro1_var.get(), filtro2_var.get(), etc.
    # Por enquanto, vamos apenas imprimir os valores para demonstração
    print("Filtro 1:", filtro1_var.get())
    print("Filtro 2:", filtro2_var.get())

# Criar a janela principal
root = tk.Tk()
root.title("Filtragem de Dados")

# Criar variáveis para armazenar os valores dos campos de filtro
filtro1_var = tk.StringVar()
filtro2_var = tk.StringVar()

# Criar rótulos e campos de entrada para os filtros
filtro1_label = ttk.Label(root, text="Filtro 1:")
filtro1_label.pack()
filtro1_entry = ttk.Entry(root, textvariable=filtro1_var)
filtro1_entry.pack()

filtro2_label = ttk.Label(root, text="Filtro 2:")
filtro2_label.pack()
filtro2_entry = ttk.Entry(root, textvariable=filtro2_var)
filtro2_entry.pack()

# Criar botão para aplicar o filtro
filtrar_button = ttk.Button(root, text="Filtrar", command=filtrar_dados)
filtrar_button.pack()

# Iniciar o loop de eventos da interface gráfica
root.mainloop()
