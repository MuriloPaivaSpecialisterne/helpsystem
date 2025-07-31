import tkinter as tk
from tkinter import messagebox
import pyodbc

class SistemaLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("HelpSystem - Login")
        self.root.geometry("400x300")
        
        # Configuração da conexão com o banco de dados
        self.dados_conexao = (
            "Driver={SQL Server};"
            "Server=Specialisterne;"
            "Database=HelpSystem;"
        )
        
        # Frame principal
        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack(expand=True)
        
        # Widgets de login
        self.label_usuario = tk.Label(self.frame, text="Usuário:")
        self.label_usuario.grid(row=0, column=0, sticky="w", pady=5)
        
        self.entry_usuario = tk.Entry(self.frame, width=30)
        self.entry_usuario.grid(row=0, column=1, pady=5)
        
        self.label_senha = tk.Label(self.frame, text="Senha:")
        self.label_senha.grid(row=1, column=0, sticky="w", pady=5)
        
        self.entry_senha = tk.Entry(self.frame, width=30, show="*")
        self.entry_senha.grid(row=1, column=1, pady=5)
        
        self.btn_login = tk.Button(self.frame, text="Login", command=self.fazer_login)
        self.btn_login.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.btn_cadastrar = tk.Button(self.frame, text="Cadastrar Novo Usuário", command=self.abrir_tela_cadastro)
        self.btn_cadastrar.grid(row=3, column=0, columnspan=2, pady=5)
    
    def conectar_banco(self):
        try:
            conexao = pyodbc.connect(self.dados_conexao)
            return conexao
        except pyodbc.Error as e:
            messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao banco de dados:\n{str(e)}")
            return None
    
    def fazer_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        
        if not usuario or not senha:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos!")
            return
        
        conexao = self.conectar_banco()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute("SELECT * FROM dbo.usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
                resultado = cursor.fetchone()
                
                if resultado:
                    messagebox.showinfo("Sucesso", f"Bem-vindo, {resultado.nome_completo}!")
                else:
                    messagebox.showerror("Erro", "Usuário ou senha incorretos!")
            except pyodbc.Error as e:
                messagebox.showerror("Erro", f"Erro ao consultar banco de dados:\n{str(e)}")
            finally:
                conexao.close()
    
    def abrir_tela_cadastro(self):
        self.tela_cadastro = tk.Toplevel(self.root)
        self.tela_cadastro.title("Cadastro de Usuário")
        self.tela_cadastro.geometry("400x400")
        
        # Widgets de cadastro
        tk.Label(self.tela_cadastro, text="Nome Completo:").pack(pady=5)
        self.entry_nome = tk.Entry(self.tela_cadastro, width=30)
        self.entry_nome.pack(pady=5)
        
        tk.Label(self.tela_cadastro, text="E-mail:").pack(pady=5)
        self.entry_email = tk.Entry(self.tela_cadastro, width=30)
        self.entry_email.pack(pady=5)
        
        tk.Label(self.tela_cadastro, text="Usuário:").pack(pady=5)
        self.entry_novo_usuario = tk.Entry(self.tela_cadastro, width=30)
        self.entry_novo_usuario.pack(pady=5)
        
        tk.Label(self.tela_cadastro, text="Senha:").pack(pady=5)
        self.entry_nova_senha = tk.Entry(self.tela_cadastro, width=30, show="*")
        self.entry_nova_senha.pack(pady=5)
        
        tk.Label(self.tela_cadastro, text="Confirmar Senha:").pack(pady=5)
        self.entry_confirma_senha = tk.Entry(self.tela_cadastro, width=30, show="*")
        self.entry_confirma_senha.pack(pady=5)
        
        tk.Button(self.tela_cadastro, text="Cadastrar", command=self.cadastrar_usuario).pack(pady=10)
    
    def cadastrar_usuario(self):
        nome = self.entry_nome.get()
        email = self.entry_email.get()
        usuario = self.entry_novo_usuario.get()
        senha = self.entry_nova_senha.get()
        confirma_senha = self.entry_confirma_senha.get()
        
        if not all([nome, email, usuario, senha, confirma_senha]):
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos!")
            return
        
        if senha != confirma_senha:
            messagebox.showerror("Erro", "As senhas não coincidem!")
            return
        
        conexao = self.conectar_banco()
        if conexao:
            try:
                cursor = conexao.cursor()
                
                # Verifica se usuário já existe
                cursor.execute("SELECT usuario FROM dbo.usuarios WHERE usuario = ?", (usuario,))
                if cursor.fetchone():
                    messagebox.showerror("Erro", "Nome de usuário já existe!")
                    return
                
                # Insere novo usuário
                cursor.execute("""
                    INSERT INTO dbo.usuarios 
                    (nome_completo, email, usuario, senha, data_cadastro) 
                    VALUES (?, ?, ?, ?, CONVERT(VARCHAR, GETDATE(), 120))
                """, (nome, email, usuario, senha))
                
                conexao.commit()
                messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
                self.tela_cadastro.destroy()
                
            except pyodbc.Error as e:
                messagebox.showerror("Erro", f"Erro ao cadastrar usuário:\n{str(e)}")
            finally:
                conexao.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaLogin(root)
    root.mainloop()