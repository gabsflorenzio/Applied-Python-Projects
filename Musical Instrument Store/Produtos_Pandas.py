import mysql.connector
import pandas as pd
import google.generativeai as genai
import json
import time
from sqlalchemy import create_engine

# Configuração da API Gemini
genai.configure(api_key="AIzaSyDKK5UsOU0mzhNnfKMqFrqZobF1qD1cTdQ")
model_name = "gemini-1.5-pro"
model = genai.GenerativeModel(model_name)

# Criação do engine SQLAlchemy para o MySQL
usuario = "Gabriel"
senha = "@Florencioti0579"
host = "localhost"
banco = "faker_test_2"

# Formata a URL de conexão
url_conexao = f"mysql+mysqlconnector://{usuario}:{senha}@{host}/{banco}"
engine = create_engine(url_conexao)

# Consulta SQL para obter os produtos
query = "SELECT * FROM produto;"
df = pd.read_sql(query, con=engine)

# Mostra os nomes das colunas para garantir que estejam corretos
print("Colunas da tabela:", df.columns)

# Função de classificação com base em IA


def classificar_produto_ia(codigo_produto, nome_produto):
    exemplo_categorias = '''
    {
      "equipamentos": [
        {"nome": "Guitarra Elétrica", "categoria": "Cordas"},
        {"nome": "Baixo Elétrico", "categoria": "Cordas"},
        {"nome": "Teclado Sintetizador", "categoria": "Teclas"},
        {"nome": "Bateria Eletrônica", "categoria": "Percussão"},
        {"nome": "Mesa de Som", "categoria": "Mixagem"},
        {"nome": "Microfone Condensador", "categoria": "Captação"},
        {"nome": "Amplificador de Guitarra", "categoria": "Amplificação"},
        {"nome": "Pedal de Efeitos", "categoria": "Processamento de Áudio"},
        {"nome": "Fone de Ouvido Profissional", "categoria": "Monitoramento"},
        {"nome": "Interface de Áudio", "categoria": "Gravação"},
        {"nome": "Controlador MIDI", "categoria": "Produção Musical"},
        {"nome": "Caixa de Som Ativa", "categoria": "Sonorização"},
        {"nome": "Equalizador Gráfico", "categoria": "Tratamento de Som"},
        {"nome": "Sampler", "categoria": "Efeitos Sonoros"},
        {"nome": "Processador de Reverb", "categoria": "Ambiência"}
      ]
    }
    '''

    prompt = f''' 
Dado o seguinte JSON de equipamentos de eletrônica musical e suas respectivas categorias exemplos:
{exemplo_categorias}

Agora, classifique o seguinte equipamento pelo seu nome, escolhendo uma das categorias existentes nos exemplos passados. 
Caso ele não se enquadre em nenhuma categoria, retorne 'Categoria não identificada'.  

Equipamento: Código: {codigo_produto}  Nome: {nome_produto}  

Não retorne o JSON de categorias, apenas o produto classificado, garantindo que o código do produto seja igual a {codigo_produto} e o nome do produto seja igual a "{nome_produto}".

No campo `codigo_produto`, coloque o código do equipamento, no campo `nome_produto` coloque o nome do equipamento e no campo `categoria` coloque a categoria que você classificou o equipamento.
Caso o equipamento não se enquadre em nenhuma categoria, retorne 'Categoria não identificada' no campo `categoria`.

Quero que me retorne SEMPRE apenas JSON no seguinte formato, sem nenhum texto adicional, não retorne "```json", apenas o valor JSON:
{{
    "codigo_produto": {codigo_produto},
    "nome_produto": "{nome_produto}", 
    "categoria": "string"
}} 
'''

    try:
        response = model.generate_content(prompt)
        produto_classificado = response.text.replace(
            "```", "").replace("json", "").strip()
        produto = json.loads(produto_classificado)
        return produto["categoria"]
    except Exception as e:
        print(f"Erro ao classificar produto {codigo_produto}: {e}")
        return "Erro IA"


# Abrindo conexão para update com mysql.connector (necessário para write)

conexao_write = mysql.connector.connect(
    host="localhost",
    user=usuario,
    password=senha,
    database=banco
)
cursor = conexao_write.cursor()

# Loop para classificar e atualizar
for _, row in df.iterrows():
    # Ajuste aqui com base nas colunas reais
    codigo = int(row["codigo"])  # ou "id" se for o nome da coluna
    nome = str(row["nome"])      # ou "nome_produto"

    categoria = classificar_produto_ia(codigo, nome)
    print(f"[{codigo}] '{nome}' → Categoria classificada: {categoria}")

    try:
        cursor.execute(
            "UPDATE produto SET categoria = %s WHERE codigo = %s",
            (categoria, codigo)
        )
        conexao_write.commit()
    except Exception as e:
        print(f"Erro ao atualizar banco para código {codigo}: {e}")

    time.sleep(1.5)  # Evita limite de requisições da API

# Encerrar conexões
cursor.close()
conexao_write.close()
