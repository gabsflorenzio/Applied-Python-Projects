import mysql.connector
from faker import Faker
import random
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

# Criando o cursor e o Faker com localidade em português
cursor = conexao.cursor()
fake = Faker('pt_BR')

# Lista estendida de nomes de produtos musicais diversos
nomes_produtos = [
    "Stratocaster Elite", "Bateria Fusion Pro", "Contrabaixo Jazz Vintage", "Piano de Cauda Digital",
    "Microfone Sem Fio X9", "Microfone Phantom Power", "Pedal de Efeito Echo", "Looper de Gravação",
    "Escudo Acústico de Microfone", "Amplificador Stage 5000", "Violino Elétrico V-Pro", "Cajón de Madeira",
    "Saxofone Sonhador", "Teclado Sinfônico", "Baixo Treme Terra", "Bateria DrumCraft Pro", "Guitarra Nova Era",
    "Microfone VoiceMaster", "Pedal de Chorus e Delay", "Caixa Orquestral", "Sintetizador Revolution", "Mesa Beat Maker",
    "Máquina de Groove", "Monitor de Estúdio S1", "Teclado Compacto Piano Roll", "Painel Acústico Pro",
    "Pedal Kick Turbo", "Caixa Snare Supreme", "Braço Articulado de Microfone", "Kit de Cordas Harmônicas",
    "Tanque de Reverb FX", "Baquetas Maple Pro", "Suporte de Microfone Tripé", "Noise Gate Pro X",
    "Pedal Overdrive Plus", "Controlador de Hi-Hat", "Mesa de Som Power Mixer 12X", "Placa de Som AudioMax",
    "Cabine Vocal Básica", "Seletor de Linha", "Fone de Ouvido Estúdio HD", "Microfone de Fita Clássico",
    "Cabeçote de Amplificador Hi-Gain", "Amplificador Valvulado Revival", "Processador Multi-FX", "Unidade de Reverb Ultra",
    "Kit de Limpeza para Escala", "Pacote de Cabos Patch", "Pedal Stompbox Vintage", "Gravador Digital H2",
    "Kit de Percussão Groove", "Captador Jazz Pro", "Afinador de Rack", "Pedal de Expressão EX",
    "Divisor de Oitava", "Teclado Master 61", "Interface de Áudio Plus", "Reprodutor de Base de Áudio",
    "Sistema In-Ear Sem Fio", "Correia de Guitarra de Couro", "Kit de Saddles para Ponte", "Pedal Duplo Kick"
]

# Marcas fictícias e reais
marcas = ["Fender", "Gibson", "Yamaha", "Roland", "Shure",
          "Ibanez", "Tama", "Pearl", "Behringer", "Boss", fake.company()]

# Gerando e inserindo os produtos
for _ in range(10):
    nome = random.choice(nomes_produtos)
    descricao = fake.sentence()
    preco = round(random.uniform(100, 5000), 2)
    marca = random.choice(marcas)

    cursor.execute(
        "INSERT INTO produto (nome, descricao, preco, marca) VALUES (%s, %s, %s, %s)",
        (nome, descricao, preco, marca)
    )

    print(f"Produto '{nome}' inserido com sucesso!")

# Commit e encerramento da conexão
conexao.commit()
cursor.close()
conexao.close()
print("Conexão encerrada com sucesso.")
