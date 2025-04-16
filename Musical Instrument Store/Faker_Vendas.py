import mysql.connector
from faker import Faker
import random
import os
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

# Conexão com o banco de dados
conexao = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

# Cursor e Faker em pt-BR
cursor = conexao.cursor()
fake = Faker("pt_BR")

# Buscar os IDs de clientes, vendedores e filiais
cursor.execute("SELECT cod_cliente FROM cliente")
clientes = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT cod_vendedor FROM vendedor")
vendedores = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT cod_filial FROM filial")
filiais = [row[0] for row in cursor.fetchall()]

# Inserção das vendas
for _ in range(50):
    cod_cliente = random.choice(clientes)
    cod_vendedor = random.choice(vendedores) if random.random() > 0.1 else None
    cod_filial = random.choice(filiais)
    data_venda = fake.date_time_between(start_date="-1y", end_date="now")
    valor_total = round(random.uniform(50, 5000), 2)

    cursor.execute("""
        INSERT INTO venda (cod_cliente, cod_vendedor, cod_filial, data_venda, valor_total) 
        VALUES (%s, %s, %s, %s, %s)
    """, (cod_cliente, cod_vendedor, cod_filial, data_venda, valor_total))

    print(f"Venda de R${valor_total} cadastrada com sucesso!")

# Commit e fechamento
conexao.commit()
cursor.close()
conexao.close()
