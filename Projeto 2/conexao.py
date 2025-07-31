import pyodbc

# Dados de conexão
dados_conexao = (
    "Driver={SQL Server};"
    "Server=Specialisterne;"
    "Database=HelpSystem;"
    #"Trusted_Connection=yes;"  Adicionado para autenticação do Windows
)


def verificar_login(usuario, senha):
    try:
        # Estabelecer conexão
        conexao = pyodbc.connect(dados_conexao)
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE usuario = ? AND senha = ?",
            (usuario, senha)
        )

        resultado = cursor.fetchone()
        conexao.close()

        return resultado is not None
    
    except Exception as e:
        print("Erro ao verificar login: {e}")
        return False


