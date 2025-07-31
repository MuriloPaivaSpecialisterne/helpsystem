import tkinter as tk
from tkinter import messagebox
import pyodbc
from datetime import datetime

dados_conexao = (
    "Driver={SQL Server};"
    "Server=Specialisterne;"
    "Database=HelpSystem;"
)

def registrar_usuario():
    nome_completo = entry_nome.get()
    email = entry_email.get()
    usuario = entry_usuario.get()
    senha = entry_senha.get()
    confirmar_senha = entry_confirmar_senha.get()

    if not all([nome_completo, email, usuario, senha, confirmar_senha]):
        messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
        return
    
    if senha != confirmar_senha:
        messagebox.showerror("Erro", "As senhas não coincidem!")
        return
    
    if len(senha) < 6:
        messagebox.showerror("Erro", "A senha deve ter pelo menos 6 caracteres!")
        return

    try:
        conexao = pyodbc.connect(dados_conexao)
        cursor = conexao.cursor()

        # Verificar se usuário já existe
        cursor.execute("SELECT usuario FROM usuarios WHERE usuario = ?", (usuario,))
        if cursor.fetchone():
            messagebox.showerror("Erro", "Usuário já existe!")
            return

        # Verificar se email já existe
        cursor.execute("SELECT email FROM usuarios WHERE email = ?", (email,))
        if cursor.fetchone():
            messagebox.showerror("Erro", "Email já cadastrado!")
            return

        
        data_cadastro = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(
            """INSERT INTO usuarios 
            (nome_completo, email, usuario, senha, data_cadastro) 
            VALUES (?, ?, ?, ?, ?)""",
            (nome_completo, email, usuario, senha, data_cadastro)
        )
        
        conexao.commit()
        conexao.close()
        
        messagebox.showinfo("Sucesso", "Usuário registrado com sucesso!")
        janela_registro.destroy()

    except pyodbc.Error as e:
        messagebox.showerror("Erro de Banco de Dados", f"Erro ao registrar usuário: {str(e)}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {str(e)}")



# Interface (mantida igual)
janela_registro = tk.Tk()
janela_registro.title("Registro de Usuário")
janela_registro.geometry("400x450")
janela_registro.configure(bg='#2b2b2b')

estilo = {
    'label': {'fg': 'white', 'bg': '#2b2b2b', 'anchor': 'w', 'font': ('Arial', 10)},
    'entry': {'width': 35, 'font': ('Arial', 10)},
    'botao': {'width': 20, 'pady': 8, 'bg': '#3b3b3b', 'fg': 'white'}
}

tk.Label(janela_registro, text="Nome Completo:", **estilo['label']).pack(pady=(15, 0), padx=25, anchor='w')
entry_nome = tk.Entry(janela_registro, **estilo['entry'])
entry_nome.pack(pady=(0, 10), padx=25)

tk.Label(janela_registro, text="Email:", **estilo['label']).pack(pady=(10, 0), padx=25, anchor='w')
entry_email = tk.Entry(janela_registro, **estilo['entry'])
entry_email.pack(pady=(0, 10), padx=25)

tk.Label(janela_registro, text="Usuário:", **estilo['label']).pack(pady=(10, 0), padx=25, anchor='w')
entry_usuario = tk.Entry(janela_registro, **estilo['entry'])
entry_usuario.pack(pady=(0, 10), padx=25)

tk.Label(janela_registro, text="Senha (mínimo 6 caracteres):", **estilo['label']).pack(pady=(10, 0), padx=25, anchor='w')
entry_senha = tk.Entry(janela_registro, show="*", **estilo['entry'])
entry_senha.pack(pady=(0, 10), padx=25)

tk.Label(janela_registro, text="Confirmar Senha:", **estilo['label']).pack(pady=(10, 0), padx=25, anchor='w')
entry_confirmar_senha = tk.Entry(janela_registro, show="*", **estilo['entry'])
entry_confirmar_senha.pack(pady=(0, 20), padx=25)

btn_registrar = tk.Button(
    janela_registro, 
    text="REGISTRAR", 
    command=registrar_usuario,
    **estilo['botao']
)
btn_registrar.pack(pady=10)

janela_registro.mainloop()