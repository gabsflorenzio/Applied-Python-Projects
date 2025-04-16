import mysql.connector
from faker import Faker
import random
import os
from dotenv import load_dotenv

# Carregar as variáveis de ambiente
load_dotenv()

# Conexão com o banco de dados usando .env
conexao = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

# Criando o cursor e o Faker
cursor = conexao.cursor()
fake = Faker("pt_BR")

# Gêneros válidos
generos = ['Masculino', 'Feminino', 'Outro', 'Prefiro não informar']

# Gerando e inserindo os clientes
for _ in range(10):
    nome = fake.name()
    cpf = fake.cpf()
    data_nascimento = fake.date_of_birth(minimum_age=18, maximum_age=80)
    genero = random.choice(generos)
    telefone = fake.phone_number()
    email = fake.email()
    endereco = fake.street_address()
    complemento = fake.word() if random.random() > 0.3 else ""
    bairro = fake.city_suffix()
    cidade = fake.city()
    estado = fake.estado_sigla()
    cep = fake.postcode()

    cursor.execute(
        """INSERT INTO cliente 
        (nome, cpf, data_nascimento, genero, telefone, email, endereco, complemento, bairro, cidade, estado, cep) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (nome, cpf, data_nascimento, genero, telefone, email,
         endereco, complemento, bairro, cidade, estado, cep)
    )

    print(f"Cliente {nome} cadastrado com sucesso!")

# Commit e fechamento
conexao.commit()
cursor.close()
conexao.close()
