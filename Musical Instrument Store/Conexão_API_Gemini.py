import google.generativeai as genai

# Configure a chave da API
API_KEY = "AIzaSyBGaU16Qnv3O_qHVXq0_u2jk-THkuhlkp0"
genai.configure(api_key=API_KEY)

# Escolher o melhor modelo disponível
# Tente "gemini-1.5-pro-latest" se houver erro
model_name = "gemini-1.5-pro-latest"

# Criar um modelo para teste
model = genai.GenerativeModel(model_name)

# Testar uma pergunta simples
try:
    response = model.generate_content(
        "Me explique a teoria da relatividade de forma simples.")
    print("Resposta da IA:", response.text)
except Exception as e:
    print("Erro ao conectar com a API:", e)
