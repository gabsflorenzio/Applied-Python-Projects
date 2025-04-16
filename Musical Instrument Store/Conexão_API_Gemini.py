import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

# Puxa a chave da API e o nome do modelo do .env
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("model_name")

# Configura a API do Gemini
genai.configure(api_key=API_KEY)

# Cria o modelo com base no nome carregado
model = genai.GenerativeModel(MODEL_NAME)

# Testa uma pergunta simples
try:
    response = model.generate_content(
        "Me explique a teoria da relatividade de forma simples.")
    print("Resposta da IA:", response.text)
except Exception as e:
    print("Erro ao conectar com a API:", e)
