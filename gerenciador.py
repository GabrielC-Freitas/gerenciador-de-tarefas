import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# Função para adicionar uma nova tarefa ao banco de dados
def adicionar_tarefa():
    nome_tarefa = entry_tarefa.get()
    descricao_tarefa = entry_descricao.get()
    data_inicio = entry_data.get()
    hora_inicio = entry_hora.get()
    
    try:
        duracao_dias = int(entry_duracao.get())
    except ValueError:
        messagebox.showwarning("Erro", "Duração precisa ser um número inteiro.")
        return

    if not nome_tarefa or not data_inicio or not hora_inicio:
        messagebox.showwarning("Erro", "Por favor, preencha todos os campos obrigatórios.")
        return

    try:
        data_formatada = datetime.strptime(data_inicio, "%d/%m/%Y")
        hora_formatada = datetime.strptime(hora_inicio, "%H:%M")
    except ValueError:
        messagebox.showwarning("Erro", "Formato de data ou hora inválido. Use DD/MM/AAAA e HH:MM.")
        return

    data_inicio = data_formatada.strftime("%Y-%m-%d")
    hora_inicio = hora_formatada.strftime("%H:%M:%S")

    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS tarefas
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, descricao TEXT, data_inicio TEXT, hora_inicio TEXT, duracao_dias INTEGER)''')

    cursor.execute("INSERT INTO tarefas (nome, descricao, data_inicio, hora_inicio, duracao_dias) VALUES (?, ?, ?, ?, ?)",
                   (nome_tarefa, descricao_tarefa, data_inicio, hora_inicio, duracao_dias))
    
    conn.commit()
    conn.close()

    messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso.")
    limpar_campos()
    listar_tarefas()

# Função para limpar os campos após adicionar uma tarefa
def limpar_campos():
    entry_tarefa.delete(0, tk.END)
    entry_descricao.delete(0, tk.END)
    entry_data.delete(0, tk.END)
    entry_hora.delete(0, tk.END)
    entry_duracao.delete(0, tk.END)

# Função para apagar uma tarefa selecionada
def apagar_tarefa():
    tarefa_selecionada = listbox_tarefas.curselection()
    if not tarefa_selecionada:
        messagebox.showwarning("Erro", "Selecione uma tarefa para apagar.")
        return

    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()

    id_tarefa = listbox_tarefas.get(tarefa_selecionada).split(":")[0]
    cursor.execute("DELETE FROM tarefas WHERE id=?", (id_tarefa,))
    
    conn.commit()
    conn.close()

    messagebox.showinfo("Sucesso", "Tarefa apagada com sucesso.")
    listar_tarefas()

# Função para listar todas as tarefas
def listar_tarefas():
    listbox_tarefas.delete(0, tk.END)

    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tarefas")  # Selecionar todas as colunas
    tarefas = cursor.fetchall()
    
    for tarefa in tarefas:
        listbox_tarefas.insert(tk.END, f"{tarefa[0]}: {tarefa[1]}")

    conn.close()

# Criar a interface gráfica
root = tk.Tk()
root.title("Gerenciador de Tarefas")

frame_adicionar = tk.Frame(root)
frame_adicionar.pack(pady=10)

label_tarefa = tk.Label(frame_adicionar, text="Tarefa:")
label_tarefa.grid(row=0, column=0, padx=5, pady=5)
entry_tarefa = tk.Entry(frame_adicionar)
entry_tarefa.grid(row=0, column=1, padx=5, pady=5)

label_descricao = tk.Label(frame_adicionar, text="Descrição:")
label_descricao.grid(row=1, column=0, padx=5, pady=5)
entry_descricao = tk.Entry(frame_adicionar)
entry_descricao.grid(row=1, column=1, padx=5, pady=5)

label_data = tk.Label(frame_adicionar, text="Data de Início (DD/MM/AAAA):")
label_data.grid(row=2, column=0, padx=5, pady=5)
entry_data = tk.Entry(frame_adicionar)
entry_data.grid(row=2, column=1, padx=5, pady=5)

label_hora = tk.Label(frame_adicionar, text="Hora de Início (HH:MM):")
label_hora.grid(row=3, column=0, padx=5, pady=5)
entry_hora = tk.Entry(frame_adicionar)
entry_hora.grid(row=3, column=1, padx=5, pady=5)

label_duracao = tk.Label(frame_adicionar, text="Duração (dias):")
label_duracao.grid(row=4, column=0, padx=5, pady=5)
entry_duracao = tk.Entry(frame_adicionar)
entry_duracao.grid(row=4, column=1, padx=5, pady=5)

button_adicionar = tk.Button(frame_adicionar, text="Adicionar Tarefa", command=adicionar_tarefa)
button_adicionar.grid(row=5, column=0, columnspan=2, pady=10)

frame_listar = tk.Frame(root)
frame_listar.pack(pady=10)

label_listar = tk.Label(frame_listar, text="Tarefas:")
label_listar.grid(row=0, column=0, padx=5, pady=5)

scrollbar = tk.Scrollbar(frame_listar, orient=tk.VERTICAL)
listbox_tarefas = tk.Listbox(frame_listar, yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox_tarefas.yview)
listbox_tarefas.grid(row=1, column=0)
scrollbar.grid(row=1, column=1, sticky="NS")

button_apagar = tk.Button(frame_listar, text="Apagar Tarefa", command=apagar_tarefa)
button_apagar.grid(row=2, column=0, pady=10)

# Criar o banco de dados SQLite para armazenar as tarefas
conn = sqlite3.connect('tarefas.db')
cursor = conn.cursor()

# Verificar se a tabela já existe
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tarefas'")
table_exists = cursor.fetchone()

# Se a tabela não existir, criá-la
if not table_exists:
    cursor.execute('''CREATE TABLE tarefas (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      nome TEXT,
                      descricao TEXT,
                      data_inicio TEXT,
                      hora_inicio TEXT,
                      duracao_dias INTEGER
                      )''')

    conn.commit()

conn.close()

# Listar as tarefas ao iniciar o aplicativo
listar_tarefas()

root.mainloop()
