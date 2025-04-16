import mysql.connector
import random
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv()

# Conexão com o banco de dados
conexao = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = conexao.cursor()

# Buscar os códigos de venda e produto existentes
cursor.execute("SELECT cod_venda FROM venda")
vendas = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT cod_produto, preco FROM produto")
produtos = cursor.fetchall()  # (cod_produto, preco)

# Controlar os pares já inseridos
pares_inseridos = set()

# Inserir 100 registros únicos
for _ in range(10):
    while True:
        cod_venda = random.choice(vendas)
        cod_produto, preco_unitario = random.choice(produtos)

        if (cod_venda, cod_produto) not in pares_inseridos:
            pares_inseridos.add((cod_venda, cod_produto))
            break

    quantidade = random.randint(1, 10)

    cursor.execute("""
        INSERT INTO venda_item (cod_venda, cod_produto, quantidade, preco_unitario)
        VALUES (%s, %s, %s, %s)
    """, (cod_venda, cod_produto, quantidade, preco_unitario))

# Commit e fechamento
conexao.commit()
cursor.close()
conexao.close()

print("Dados inseridos com sucesso na tabela 'venda_item'!")
