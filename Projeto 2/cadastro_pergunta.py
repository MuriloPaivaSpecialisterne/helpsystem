import pyodbc
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime

class PerguntasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Perguntas e Respostas")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        self.root.configure(bg='#f0f0f0')
        
        # Configuração do estilo
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 14, 'bold'))
        
        self.criar_widgets()
    
    def criar_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=BOTH, expand=True)
        
        # Cabeçalho
        header = ttk.Label(main_frame, text="Cadastro de Nova Pergunta", style='Header.TLabel')
        header.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Campo Título
        ttk.Label(main_frame, text="Título:").grid(row=1, column=0, sticky=W, pady=(0, 5))
        self.entry_titulo = ttk.Entry(main_frame, width=60, font=('Arial', 10))
        self.entry_titulo.grid(row=2, column=0, columnspan=2, pady=(0, 15))
        
        # Campo Pergunta
        ttk.Label(main_frame, text="Pergunta:").grid(row=3, column=0, sticky=W, pady=(0, 5))
        self.text_pergunta = Text(main_frame, width=60, height=15, font=('Arial', 10), 
                                 wrap=WORD, padx=5, pady=5)
        scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=self.text_pergunta.yview)
        self.text_pergunta.configure(yscrollcommand=scrollbar.set)
        
        self.text_pergunta.grid(row=4, column=0, pady=(0, 15))
        scrollbar.grid(row=4, column=1, sticky='ns', pady=(0, 15))
        
        # Botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=(10, 0))
        
        self.btn_cadastrar = ttk.Button(btn_frame, text="Cadastrar Pergunta", 
                                      command=self.cadastrar_pergunta, style='TButton')
        self.btn_cadastrar.pack(side=LEFT, padx=5)
        
        self.btn_limpar = ttk.Button(btn_frame, text="Limpar Campos", 
                                   command=self.limpar_campos)
        self.btn_limpar.pack(side=LEFT, padx=5)
        
        # Status bar
        self.status_var = StringVar()
        self.status_var.set("Pronto para cadastrar nova pergunta")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                             relief=SUNKEN, anchor=W)
        status_bar.grid(row=6, column=0, columnspan=2, sticky=EW, pady=(20, 0))
    
    def conectar_banco(self):
        try:
            conexao = pyodbc.connect(
                "Driver={SQL Server};"
                "Server=Specialisterne;"
                "Database=HelpSystem;"
            )
            return conexao
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao conectar ao banco: {e}")
            return None
    
    def cadastrar_pergunta(self):
        titulo = self.entry_titulo.get()
        pergunta = self.text_pergunta.get("1.0", END).strip()
        usuario_id = 1  # Substituir pelo ID do usuário logado
        
        if not titulo or not pergunta:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        
        try:
            self.status_var.set("Conectando ao banco de dados...")
            self.root.update()
            
            conexao = self.conectar_banco()
            if not conexao:
                return
                
            cursor = conexao.cursor()
            
            data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            self.status_var.set("Cadastrando pergunta...")
            self.root.update()
            
            cursor.execute(
                "INSERT INTO perguntas (titulo, pergunta, usuario_id, data_criacao) VALUES (?, ?, ?, ?)",
                (titulo, pergunta, usuario_id, data_atual)
            )
            
            conexao.commit()
            messagebox.showinfo("Sucesso", "Pergunta cadastrada com sucesso!")
            self.limpar_campos()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar pergunta: {e}")
        finally:
            self.status_var.set("Pronto para cadastrar nova pergunta")
            if 'conexao' in locals():
                conexao.close()
    
    def limpar_campos(self):
        self.entry_titulo.delete(0, END)
        self.text_pergunta.delete("1.0", END)
        self.status_var.set("Campos limpos. Pronto para nova pergunta.")

if __name__ == "__main__":
    root = Tk()
    app = PerguntasApp(root)
    root.mainloop()