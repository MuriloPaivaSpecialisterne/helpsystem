import tkinter as tk
from tkinter import messagebox
from conexao import verificar_login


def validar_login():
    usuario = texto_usuario.get()
    senha = texto_senha.get()

    if verificar_login(usuario, senha):
        messagebox.showinfo("Sucesso", "Login válido!")
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos!")




    
# CRIAÇÃO DA JANELA PRINCIPAL
app = tk.Tk()
app.title('Tela de Login')
app.geometry('300x300')
app.configure(bg='#2b2b2b')  # aparência escura manual

# CAMPO USUÁRIO
label_usuario = tk.Label(app, text='Usuário', fg='white', bg='#2b2b2b')
label_usuario.pack(pady=10)

texto_usuario = tk.Entry(app)
texto_usuario.pack(pady=10)

# CAMPO SENHA
label_senha = tk.Label(app, text='Senha', fg='white', bg='#2b2b2b')
label_senha.pack(pady=10)

texto_senha = tk.Entry(app, show='*')
texto_senha.pack(pady=10)

# BOTÃO LOGIN
btn_login = tk.Button(app, text='LOGIN', command=validar_login)
btn_login.pack(pady=10)



# INICIAR A APLICAÇÃO
app.mainloop()