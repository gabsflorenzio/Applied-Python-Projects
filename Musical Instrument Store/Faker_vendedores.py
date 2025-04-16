import mysql.connector
from faker import Faker
import random
import os
from dotenv import load_dotenv

# Carregando as variáveis de ambiente do arquivo .env
load_dotenv()

# Conexão com o banco de dados
conexao = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

# Criando o cursor e o Faker
cursor = conexao.cursor()
fake = Faker("pt_BR")

# Obtendo os IDs das filiais existentes
cursor.execute("SELECT cod_filial FROM filial")
filiais = [row[0] for row in cursor.fetchall()]

# Lista de faixas salariais possíveis
faixa_salarial = [2000.00, 2500.00, 3000.00, 3500.00, 4000.00]

# Gerando e inserindo os vendedores
for _ in range(10):
    nome = fake.name()
    cpf = fake.cpf()
    telefone = fake.phone_number()
    email = fake.email()
    cod_filial = random.choice(filiais)
    data_admissao = fake.date_between(start_date="-5y", end_date="today")
    salario = random.choice(faixa_salarial)

    cursor.execute(
        "INSERT INTO vendedor (nome, cpf, telefone, email, cod_filial, data_admissao, salario) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (nome, cpf, telefone, email, cod_filial, data_admissao, salario)
    )

    print(f"Vendedor {nome} cadastrado com sucesso!")

# Commit e fechamento
conexao.commit()
cursor.close()
conexao.close()
