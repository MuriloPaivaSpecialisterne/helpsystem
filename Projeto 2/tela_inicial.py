import pyodbc
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
from tkinter.font import Font

class HelpSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Help System - Perguntas e Respostas")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Estilos
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 14, 'bold'))
        self.style.configure('Question.TLabel', font=('Arial', 11, 'bold'), foreground='#2c3e50')
        
        # Fontes
        self.title_font = Font(family='Arial', size=12, weight='bold')
        self.normal_font = Font(family='Arial', size=10)
        
        # Variáveis
        self.current_user = {"id": 1, "nome": "Usuário Teste"}  # Simula usuário logado
        
        self.create_main_menu()
    
    def create_main_menu(self):
        # Limpa a tela atual
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=BOTH, expand=True)
        
        # Cabeçalho
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=X, pady=(0, 20))
        
        ttk.Label(header_frame, 
                text=f"Bem-vindo, {self.current_user['nome']}",
                style='Header.TLabel').pack(side=LEFT)
        
        btn_frame = ttk.Frame(header_frame)
        btn_frame.pack(side=RIGHT)
        
        ttk.Button(btn_frame, text="Nova Pergunta", 
                 command=self.show_new_question_form).pack(side=LEFT, padx=5)
        
        # Lista de perguntas
        questions_frame = ttk.LabelFrame(main_frame, text="Perguntas Recentes", padding=10)
        questions_frame.pack(fill=BOTH, expand=True)
        
        # Treeview para listar perguntas
        columns = ('id', 'titulo', 'autor', 'data')
        self.questions_tree = ttk.Treeview(questions_frame, columns=columns, show='headings')
        
        self.questions_tree.heading('id', text='ID')
        self.questions_tree.heading('titulo', text='Título')
        self.questions_tree.heading('autor', text='Autor')
        self.questions_tree.heading('data', text='Data')
        
        self.questions_tree.column('id', width=50, anchor='center')
        self.questions_tree.column('titulo', width=300)
        self.questions_tree.column('autor', width=150)
        self.questions_tree.column('data', width=120)
        
        scrollbar = ttk.Scrollbar(questions_frame, orient=VERTICAL, command=self.questions_tree.yview)
        self.questions_tree.configure(yscrollcommand=scrollbar.set)
        
        self.questions_tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        # Botão para visualizar/responder
        ttk.Button(main_frame, text="Visualizar/Responder", 
                  command=self.show_question_detail).pack(pady=(10, 0))
        
        # Carrega as perguntas
        self.load_questions()
        
        # Configura evento de duplo clique
        self.questions_tree.bind('<Double-1>', lambda e: self.show_question_detail())
    
    def load_questions(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT p.id, p.titulo, u.nome_completo, p.data_criacao 
                FROM perguntas p
                JOIN usuarios u ON p.usuario_id = u.id
                ORDER BY p.data_criacao DESC
            """)
            
            # Limpa a treeview
            for item in self.questions_tree.get_children():
                self.questions_tree.delete(item)
            
            # Adiciona os resultados
            for row in cursor.fetchall():
                self.questions_tree.insert('', 'end', values=row)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar perguntas: {e}")
        finally:
            if 'conn' in locals():
                conn.close()
    
    def show_question_detail(self):
        selected_item = self.questions_tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione uma pergunta primeiro!")
            return
            
        question_id = self.questions_tree.item(selected_item[0])['values'][0]
        
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            
            # Obtém detalhes da pergunta
            cursor.execute("""
                SELECT p.titulo, p.pergunta, u.nome_completo, p.data_criacao 
                FROM perguntas p
                JOIN usuarios u ON p.usuario_id = u.id
                WHERE p.id = ?
            """, (question_id,))
            
            question_data = cursor.fetchone()
            
            # Obtém respostas
            cursor.execute("""
                SELECT r.resposta, u.nome_completo, r.data_resposta 
                FROM respostas r
                JOIN usuarios u ON r.usuario_id = u.id
                WHERE r.pergunta_id = ?
                ORDER BY r.data_resposta
            """, (question_id,))
            
            answers = cursor.fetchall()
            
            # Cria a janela de detalhes
            self.show_question_detail_window(question_id, question_data, answers)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar detalhes: {e}")
        finally:
            if 'conn' in locals():
                conn.close()
    
    def show_question_detail_window(self, question_id, question_data, answers):
        detail_window = Toplevel(self.root)
        detail_window.title(f"Pergunta #{question_id}")
        detail_window.geometry("800x600")
        
        # Frame principal
        main_frame = ttk.Frame(detail_window, padding="20")
        main_frame.pack(fill=BOTH, expand=True)
        
        # Exibe a pergunta
        question_frame = ttk.LabelFrame(main_frame, text="Pergunta", padding=10)
        question_frame.pack(fill=X, pady=(0, 15))
        
        ttk.Label(question_frame, text=question_data[0], style='Question.TLabel').pack(anchor=W)
        ttk.Label(question_frame, text=f"Por: {question_data[2]} em {question_data[3]}").pack(anchor=W, pady=(5, 10))
        
        question_text = Text(question_frame, wrap=WORD, height=8, font=self.normal_font)
        question_text.insert(END, question_data[1])
        question_text.config(state=DISABLED)
        question_text.pack(fill=X)
        
        # Respostas
        answers_frame = ttk.LabelFrame(main_frame, text="Respostas", padding=10)
        answers_frame.pack(fill=BOTH, expand=True)
        
        canvas = Canvas(answers_frame)
        scrollbar = ttk.Scrollbar(answers_frame, orient=VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        if answers:
            for answer in answers:
                self.create_answer_card(scrollable_frame, answer)
        else:
            ttk.Label(scrollable_frame, text="Nenhuma resposta ainda.").pack(pady=10)
        
        # Campo para nova resposta
        reply_frame = ttk.Frame(main_frame)
        reply_frame.pack(fill=X, pady=(15, 0))
        
        ttk.Label(reply_frame, text="Sua Resposta:").pack(anchor=W)
        
        self.answer_text = Text(reply_frame, wrap=WORD, height=5, font=self.normal_font)
        self.answer_text.pack(fill=X, pady=(5, 0))
        
        btn_frame = ttk.Frame(reply_frame)
        btn_frame.pack(fill=X, pady=(10, 0))
        
        ttk.Button(btn_frame, text="Enviar Resposta", 
                  command=lambda: self.submit_answer(question_id, detail_window)).pack(side=LEFT)
    
    def create_answer_card(self, parent, answer_data):
        card = ttk.Frame(parent, borderwidth=1, relief="solid", padding=10)
        card.pack(fill=X, pady=5)
        
        ttk.Label(card, text=f"Por: {answer_data[1]} em {answer_data[2]}").pack(anchor=W)
        
        answer_text = Text(card, wrap=WORD, height=4, font=self.normal_font)
        answer_text.insert(END, answer_data[0])
        answer_text.config(state=DISABLED)
        answer_text.pack(fill=X, pady=(5, 0))
    
    def submit_answer(self, question_id, window):
        resposta = self.answer_text.get("1.0", END).strip()
        
        if not resposta:
            messagebox.showwarning("Aviso", "Digite sua resposta antes de enviar!")
            return
        
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            
            data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute(
                "INSERT INTO respostas (pergunta_id, usuario_id, resposta, data_resposta) VALUES (?, ?, ?, ?)",
                (question_id, self.current_user['id'], resposta, data_atual)
            )
            
            conn.commit()
            messagebox.showinfo("Sucesso", "Resposta enviada com sucesso!")
            window.destroy()
            self.show_question_detail()  # Recarrega a pergunta
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao enviar resposta: {e}")
        finally:
            if 'conn' in locals():
                conn.close()
    
    def show_new_question_form(self):
        form_window = Toplevel(self.root)
        form_window.title("Nova Pergunta")
        form_window.geometry("600x500")
        
        # Frame principal
        main_frame = ttk.Frame(form_window, padding="20")
        main_frame.pack(fill=BOTH, expand=True)
        
        ttk.Label(main_frame, text="Nova Pergunta", style='Header.TLabel').pack(pady=(0, 20))
        
        # Campo Título
        ttk.Label(main_frame, text="Título:").pack(anchor=W)
        title_entry = ttk.Entry(main_frame, width=60, font=self.normal_font)
        title_entry.pack(fill=X, pady=(0, 15))
        
        # Campo Pergunta
        ttk.Label(main_frame, text="Descreva sua pergunta:").pack(anchor=W)
        question_text = Text(main_frame, wrap=WORD, height=15, font=self.normal_font)
        scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=question_text.yview)
        question_text.configure(yscrollcommand=scrollbar.set)
        
        question_text.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        # Botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=X, pady=(15, 0))
        
        ttk.Button(btn_frame, text="Cancelar", 
                 command=form_window.destroy).pack(side=RIGHT, padx=5)
        
        ttk.Button(btn_frame, text="Enviar Pergunta", 
                 command=lambda: self.submit_new_question(
                     title_entry.get(), 
                     question_text.get("1.0", END).strip(),
                     form_window
                 )).pack(side=RIGHT)
    
    def submit_new_question(self, titulo, pergunta, window):
        if not titulo or not pergunta:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            
            data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute(
                "INSERT INTO perguntas (titulo, pergunta, usuario_id, data_criacao) VALUES (?, ?, ?, ?)",
                (titulo, pergunta, self.current_user['id'], data_atual)
            )
            
            conn.commit()
            messagebox.showinfo("Sucesso", "Pergunta cadastrada com sucesso!")
            window.destroy()
            self.load_questions()  # Atualiza a lista de perguntas
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao cadastrar pergunta: {e}")
        finally:
            if 'conn' in locals():
                conn.close()
    
    def connect_db(self):
        try:
            conn = pyodbc.connect(
                "Driver={SQL Server};"
                "Server=Specialisterne;"
                "Database=HelpSystem;"
            )
            return conn
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao conectar ao banco: {e}")
            return None

if __name__ == "__main__":
    root = Tk()
    app = HelpSystemApp(root)
    root.mainloop()
    