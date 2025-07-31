import tkinter as tk
from tkinter import messagebox, ttk
import pyodbc

class Aplicacao:
    def __init__(self, root):
        self.root = root
        self.root.title("HelpSystem")
        self.root.geometry("800x600")
        
        # Configuração da conexão com o banco de dados
        self.dados_conexao = (
            "Driver={SQL Server};"
            "Server=Specialisterne;"
            "Database=HelpSystem;"
        )
        
        # Variável para armazenar informações do usuário logado
        self.usuario_logado = None
        
        # Mostrar tela de login inicialmente
        self.mostrar_tela_login()
    
    def conectar_banco(self):
        try:
            conexao = pyodbc.connect(self.dados_conexao)
            return conexao
        except pyodbc.Error as e:
            messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao banco de dados:\n{str(e)}")
            return None
    
    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def mostrar_tela_login(self):
        self.limpar_tela()
        
        # Frame principal
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)
        
        # Logo ou título
        tk.Label(frame, text="HelpSystem", font=("Arial", 24)).grid(row=0, column=0, columnspan=2, pady=20)
        
        # Widgets de login
        tk.Label(frame, text="Usuário:").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_usuario = tk.Entry(frame, width=30)
        self.entry_usuario.grid(row=1, column=1, pady=5)
        
        tk.Label(frame, text="Senha:").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_senha = tk.Entry(frame, width=30, show="*")
        self.entry_senha.grid(row=2, column=1, pady=5)
        
        tk.Button(frame, text="Login", command=self.fazer_login).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(frame, text="Cadastrar Novo Usuário", command=self.mostrar_tela_cadastro).grid(row=4, column=0, columnspan=2, pady=5)
    
    def mostrar_tela_cadastro(self):
        self.limpar_tela()
        
        # Frame principal
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)
        
        tk.Label(frame, text="Cadastro de Usuário", font=("Arial", 18)).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Widgets de cadastro
        tk.Label(frame, text="Nome Completo:").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_nome = tk.Entry(frame, width=30)
        self.entry_nome.grid(row=1, column=1, pady=5)
        
        tk.Label(frame, text="E-mail:").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_email = tk.Entry(frame, width=30)
        self.entry_email.grid(row=2, column=1, pady=5)
        
        tk.Label(frame, text="Usuário:").grid(row=3, column=0, sticky="w", pady=5)
        self.entry_novo_usuario = tk.Entry(frame, width=30)
        self.entry_novo_usuario.grid(row=3, column=1, pady=5)
        
        tk.Label(frame, text="Senha:").grid(row=4, column=0, sticky="w", pady=5)
        self.entry_nova_senha = tk.Entry(frame, width=30, show="*")
        self.entry_nova_senha.grid(row=4, column=1, pady=5)
        
        tk.Label(frame, text="Confirmar Senha:").grid(row=5, column=0, sticky="w", pady=5)
        self.entry_confirma_senha = tk.Entry(frame, width=30, show="*")
        self.entry_confirma_senha.grid(row=5, column=1, pady=5)
        
        tk.Button(frame, text="Cadastrar", command=self.cadastrar_usuario).grid(row=6, column=0, columnspan=2, pady=10)
        tk.Button(frame, text="Voltar para Login", command=self.mostrar_tela_login).grid(row=7, column=0, columnspan=2, pady=5)
    
    def mostrar_tela_inicial(self):
        self.limpar_tela()
        
        # Barra de menu
        menubar = tk.Menu(self.root)
        
        # Menu do usuário
        menu_usuario = tk.Menu(menubar, tearoff=0)
        menu_usuario.add_command(label="Meu Perfil", command=self.mostrar_perfil)
        menu_usuario.add_separator()
        menu_usuario.add_command(label="Sair", command=self.mostrar_tela_login)
        menubar.add_cascade(label="Usuário", menu=menu_usuario)
        
        # Menu de ajuda
        menu_ajuda = tk.Menu(menubar, tearoff=0)
        menu_ajuda.add_command(label="Sobre", command=self.mostrar_sobre)
        menubar.add_cascade(label="Ajuda", menu=menu_ajuda)
        
        self.root.config(menu=menubar)
        
        # Conteúdo principal
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True, fill=tk.BOTH)
        
        tk.Label(frame, text=f"Bem-vindo, {self.usuario_logado.nome_completo}!", font=("Arial", 16)).pack(pady=10)
        
        # Botões principais
        tk.Button(frame, text="Ver Todas as Perguntas", command=self.carregar_todas_perguntas).pack(pady=10)
        tk.Button(frame, text="Minhas Perguntas", command=self.mostrar_minhas_perguntas).pack(pady=10)
        tk.Button(frame, text="Minhas Respostas", command=self.mostrar_minhas_respostas).pack(pady=10)
        tk.Button(frame, text="Nova Pergunta", command=self.nova_pergunta).pack(pady=10)
    
    def mostrar_minhas_perguntas(self):
        self.limpar_conteudo()
        
        frame = tk.Frame(self.root)
        frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        tk.Label(frame, text="Minhas Perguntas", font=("Arial", 14)).pack(pady=10)
        
        # Treeview para mostrar as perguntas
        self.tree_minhas_perguntas = ttk.Treeview(frame, columns=("ID", "Título", "Data"), show="headings")
        self.tree_minhas_perguntas.heading("ID", text="ID")
        self.tree_minhas_perguntas.heading("Título", text="Título")
        self.tree_minhas_perguntas.heading("Data", text="Data")
        
        # Barra de rolagem
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree_minhas_perguntas.yview)
        self.tree_minhas_perguntas.configure(yscrollcommand=scrollbar.set)
        
        self.tree_minhas_perguntas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Carregar perguntas do usuário
        self.atualizar_minhas_perguntas()
        
        # Botão voltar
        tk.Button(frame, text="Voltar", command=self.mostrar_tela_inicial).pack(pady=10)
    
    def mostrar_minhas_respostas(self):
        self.limpar_conteudo()
        
        frame = tk.Frame(self.root)
        frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        tk.Label(frame, text="Minhas Respostas", font=("Arial", 14)).pack(pady=10)
        
        # Treeview para mostrar as respostas
        self.tree_minhas_respostas = ttk.Treeview(frame, columns=("ID", "Pergunta", "Data"), show="headings")
        self.tree_minhas_respostas.heading("ID", text="ID")
        self.tree_minhas_respostas.heading("Pergunta", text="Pergunta")
        self.tree_minhas_respostas.heading("Data", text="Data")
        
        # Barra de rolagem
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree_minhas_respostas.yview)
        self.tree_minhas_respostas.configure(yscrollcommand=scrollbar.set)
        
        self.tree_minhas_respostas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Carregar respostas do usuário
        self.atualizar_minhas_respostas()
        
        # Botão voltar
        tk.Button(frame, text="Voltar", command=self.mostrar_tela_inicial).pack(pady=10)
    
    def limpar_conteudo(self):
        # Remove todos os widgets exceto o menu
        for widget in self.root.winfo_children():
            if not isinstance(widget, tk.Menu):
                widget.destroy()
    
    def carregar_todas_perguntas(self):
        self.limpar_conteudo()
        
        frame = tk.Frame(self.root)
        frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        tk.Label(frame, text="Todas as Perguntas", font=("Arial", 14)).pack(pady=10)
        
        # Treeview para mostrar as perguntas
        self.tree_perguntas = ttk.Treeview(frame, columns=("ID", "Título", "Autor", "Data"), show="headings")
        self.tree_perguntas.heading("ID", text="ID")
        self.tree_perguntas.heading("Título", text="Título")
        self.tree_perguntas.heading("Autor", text="Autor")
        self.tree_perguntas.heading("Data", text="Data")
        self.tree_perguntas.column("ID", width=50)
        self.tree_perguntas.column("Título", width=300)
        self.tree_perguntas.column("Autor", width=150)
        self.tree_perguntas.column("Data", width=100)
        
        # Barra de rolagem
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree_perguntas.yview)
        self.tree_perguntas.configure(yscrollcommand=scrollbar.set)
        
        self.tree_perguntas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botão para responder
        btn_responder = tk.Button(frame, text="Responder Pergunta Selecionada", 
                                command=self.responder_pergunta_selecionada)
        btn_responder.pack(pady=10)
        
        # Botão voltar
        tk.Button(frame, text="Voltar", command=self.mostrar_tela_inicial).pack(pady=10)
        
        # Carregar perguntas do banco de dados
        self.atualizar_lista_perguntas()
    
    def atualizar_lista_perguntas(self):
        # Limpa a treeview
        for item in self.tree_perguntas.get_children():
            self.tree_perguntas.delete(item)
        
        # Busca perguntas no banco de dados
        conexao = self.conectar_banco()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute("""
                    SELECT p.id, p.titulo, u.nome_completo, p.data_criacao 
                    FROM dbo.perguntas p
                    JOIN dbo.usuarios u ON p.usuario_id = u.id
                    ORDER BY p.data_criacao DESC
                """)
                
                for pergunta in cursor.fetchall():
                    self.tree_perguntas.insert("", tk.END, values=pergunta)
                    
            except pyodbc.Error as e:
                messagebox.showerror("Erro", f"Erro ao carregar perguntas:\n{str(e)}")
            finally:
                conexao.close()
    
    def atualizar_minhas_perguntas(self):
        # Limpa a treeview
        for item in self.tree_minhas_perguntas.get_children():
            self.tree_minhas_perguntas.delete(item)
        
        # Busca perguntas do usuário no banco de dados
        conexao = self.conectar_banco()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute("""
                    SELECT id, titulo, data_criacao 
                    FROM dbo.perguntas 
                    WHERE usuario_id = ?
                    ORDER BY data_criacao DESC
                """, (self.usuario_logado.id,))
                
                for pergunta in cursor.fetchall():
                    self.tree_minhas_perguntas.insert("", tk.END, values=pergunta)
                    
            except pyodbc.Error as e:
                messagebox.showerror("Erro", f"Erro ao carregar perguntas:\n{str(e)}")
            finally:
                conexao.close()
    
    def atualizar_minhas_respostas(self):
        # Limpa a treeview
        for item in self.tree_minhas_respostas.get_children():
            self.tree_minhas_respostas.delete(item)
        
        # Busca respostas do usuário no banco de dados
        conexao = self.conectar_banco()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute("""
                    SELECT r.id, p.titulo, r.data_resposta 
                    FROM dbo.respostas r
                    JOIN dbo.perguntas p ON r.pergunta_id = p.id
                    WHERE r.usuario_id = ?
                    ORDER BY r.data_resposta DESC
                """, (self.usuario_logado.id,))
                
                for resposta in cursor.fetchall():
                    self.tree_minhas_respostas.insert("", tk.END, values=resposta)
                    
            except pyodbc.Error as e:
                messagebox.showerror("Erro", f"Erro ao carregar respostas:\n{str(e)}")
            finally:
                conexao.close()
    
    def responder_pergunta_selecionada(self):
        # Obtém a pergunta selecionada
        selecionada = self.tree_perguntas.focus()
        if not selecionada:
            messagebox.showwarning("Aviso", "Selecione uma pergunta para responder!")
            return
        
        item = self.tree_perguntas.item(selecionada)
        pergunta_id = item['values'][0]
        pergunta_titulo = item['values'][1]
        
        # Janela para resposta
        resposta_janela = tk.Toplevel(self.root)
        resposta_janela.title(f"Responder: {pergunta_titulo}")
        resposta_janela.geometry("600x400")
        
        tk.Label(resposta_janela, text=f"Respondendo à pergunta: {pergunta_titulo}", 
                font=("Arial", 12)).pack(pady=10)
        
        # Área de texto para a resposta
        self.text_resposta = tk.Text(resposta_janela, height=15, width=70)
        self.text_resposta.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Botão para submeter a resposta
        btn_submeter = tk.Button(resposta_janela, text="Enviar Resposta", 
                               command=lambda: self.enviar_resposta(pergunta_id, resposta_janela))
        btn_submeter.pack(pady=10)
    
    def enviar_resposta(self, pergunta_id, janela):
        resposta = self.text_resposta.get("1.0", tk.END).strip()
        
        if not resposta:
            messagebox.showwarning("Aviso", "A resposta não pode estar vazia!")
            return
        
        conexao = self.conectar_banco()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute("""
                    INSERT INTO dbo.respostas 
                    (pergunta_id, usuario_id, resposta, data_resposta) 
                    VALUES (?, ?, ?, CONVERT(VARCHAR, GETDATE(), 120))
                """, (pergunta_id, self.usuario_logado.id, resposta))
                
                conexao.commit()
                messagebox.showinfo("Sucesso", "Resposta enviada com sucesso!")
                janela.destroy()
                self.atualizar_lista_perguntas()  # Atualiza a lista de perguntas
                self.atualizar_minhas_respostas()  # Atualiza minhas respostas
                
            except pyodbc.Error as e:
                messagebox.showerror("Erro", f"Erro ao enviar resposta:\n{str(e)}")
            finally:
                conexao.close()
    
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
                    self.usuario_logado = resultado
                    self.mostrar_tela_inicial()
                else:
                    messagebox.showerror("Erro", "Usuário ou senha incorretos!")
            except pyodbc.Error as e:
                messagebox.showerror("Erro", f"Erro ao consultar banco de dados:\n{str(e)}")
            finally:
                conexao.close()
    
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
                
                # Verifica se email já existe
                cursor.execute("SELECT email FROM dbo.usuarios WHERE email = ?", (email,))
                if cursor.fetchone():
                    messagebox.showerror("Erro", "E-mail já cadastrado!")
                    return
                
                # Insere novo usuário
                cursor.execute("""
                    INSERT INTO dbo.usuarios 
                    (nome_completo, email, usuario, senha, data_cadastro) 
                    VALUES (?, ?, ?, ?, CONVERT(VARCHAR, GETDATE(), 120))
                """, (nome, email, usuario, senha))
                
                conexao.commit()
                messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
                self.mostrar_tela_login()
                
            except pyodbc.Error as e:
                messagebox.showerror("Erro", f"Erro ao cadastrar usuário:\n{str(e)}")
            finally:
                conexao.close()
    
    def nova_pergunta(self):
        nova_janela = tk.Toplevel(self.root)
        nova_janela.title("Nova Pergunta")
        nova_janela.geometry("600x400")
        
        tk.Label(nova_janela, text="Nova Pergunta", font=("Arial", 14)).pack(pady=10)
        
        frame = tk.Frame(nova_janela, padx=20, pady=10)
        frame.pack(expand=True, fill=tk.BOTH)
        
        tk.Label(frame, text="Título:").pack(anchor="w", pady=5)
        entry_titulo = tk.Entry(frame, width=50)
        entry_titulo.pack(fill=tk.X, pady=5)
        
        tk.Label(frame, text="Pergunta:").pack(anchor="w", pady=5)
        text_pergunta = tk.Text(frame, height=10, width=50)
        text_pergunta.pack(fill=tk.BOTH, expand=True, pady=5)
        
        def publicar_pergunta():
            titulo = entry_titulo.get()
            pergunta = text_pergunta.get("1.0", tk.END).strip()
            
            if not titulo or not pergunta:
                messagebox.showwarning("Aviso", "Por favor, preencha todos os campos!")
                return
            
            conexao = self.conectar_banco()
            if conexao:
                try:
                    cursor = conexao.cursor()
                    cursor.execute("""
                        INSERT INTO dbo.perguntas 
                        (titulo, pergunta, usuario_id, data_criacao) 
                        VALUES (?, ?, ?, CONVERT(VARCHAR, GETDATE(), 120))
                    """, (titulo, pergunta, self.usuario_logado.id))
                    
                    conexao.commit()
                    messagebox.showinfo("Sucesso", "Pergunta publicada com sucesso!")
                    nova_janela.destroy()
                    self.atualizar_lista_perguntas()
                    self.atualizar_minhas_perguntas()
                except pyodbc.Error as e:
                    messagebox.showerror("Erro", f"Erro ao publicar pergunta:\n{str(e)}")
                finally:
                    conexao.close()
        
        tk.Button(frame, text="Publicar Pergunta", command=publicar_pergunta).pack(pady=10)
    
    def mostrar_perfil(self):
        if not self.usuario_logado:
            return
        
        perfil = tk.Toplevel(self.root)
        perfil.title("Meu Perfil")
        perfil.geometry("400x300")
        
        tk.Label(perfil, text="Informações do Perfil", font=("Arial", 14)).pack(pady=10)
        
        frame = tk.Frame(perfil, padx=20, pady=10)
        frame.pack(expand=True)
        
        tk.Label(frame, text=f"Nome: {self.usuario_logado.nome_completo}").pack(anchor="w", pady=5)
        tk.Label(frame, text=f"E-mail: {self.usuario_logado.email}").pack(anchor="w", pady=5)
        tk.Label(frame, text=f"Usuário: {self.usuario_logado.usuario}").pack(anchor="w", pady=5)
        tk.Label(frame, text=f"Data de Cadastro: {self.usuario_logado.data_cadastro}").pack(anchor="w", pady=5)
    
    def mostrar_sobre(self):
        sobre = tk.Toplevel(self.root)
        sobre.title("Sobre o HelpSystem")
        sobre.geometry("300x200")
        
        tk.Label(sobre, text="HelpSystem", font=("Arial", 16)).pack(pady=10)
        tk.Label(sobre, text="Sistema de Perguntas e Respostas").pack(pady=5)
        tk.Label(sobre, text="Versão 1.0").pack(pady=5)
        tk.Label(sobre, text="Desenvolvido por [Seu Nome]").pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacao(root)
    root.mainloop()