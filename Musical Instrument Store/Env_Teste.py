import os
from dotenv import load_dotenv


# carregar as variáveis do .env
load_dotenv()

# obtendo os dados
conexao = os.getenv("conexao")
banco = os.getenv("banco")
port = os.getenv("port")
usuario = os.getenv("usuario")
senha = os.getenv("senha")

# exibir os dados lidos
print("🔌 Conectando ao banco de dados...")
print(f'🧠 Conexão: {conexao}')
print(f'📦 Banco: {banco}')
print(f'📍 Porta: {port}')
print(f'👤 Usuário: {usuario}')
print(f'🔑 Senha: {senha}')
print("✅ Conexão estabelecida com sucesso (simulada).")
