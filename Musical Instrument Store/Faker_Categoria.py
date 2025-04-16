import mysql.connector
import os
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

# Conexão com o banco de dados usando as variáveis do .env
conexao = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

# Criando o cursor
cursor = conexao.cursor()

# Selecionar todos os cod_produto da tabela produto
cursor.execute("SELECT cod_produto FROM produto")

# Recuperar todos os cod_produto
produtos = cursor.fetchall()

# Para cada cod_produto, vamos verificar se já existe uma categoria associada
for produto in produtos:
    cod_produto = produto[0]  # Aqui pegamos o cod_produto de cada linha

    # Verificar se o cod_produto já tem uma categoria associada
    cursor.execute(
        "SELECT COUNT(*) FROM categoria WHERE cod_produto = %s", (cod_produto,))
    resultado = cursor.fetchone()

    # Se não tiver uma categoria associada, insira uma nova categoria
    if resultado[0] == 0:  # Se a contagem for 0, significa que não existe
        cursor.execute(
            "INSERT INTO categoria (cod_produto, nome_categoria) VALUES (%s, %s)",
            (cod_produto, "")  # Aqui usamos uma string vazia como valor temporário
        )
        print(
            f"cod_produto {cod_produto} inserido na tabela categoria com sucesso!")
    else:
        print(
            f"cod_produto {cod_produto} já tem categoria associada, ignorado.")

# Commit e encerramento da conexão
conexao.commit()
cursor.close()
conexao.close()
print("Conexão encerrada com sucesso.")
