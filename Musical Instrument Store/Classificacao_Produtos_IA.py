import mysql.connector
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

# --- CARREGAR VARIÁVEIS DE AMBIENTE ---
load_dotenv()

# --- CONFIGURAÇÃO DA API GEMINI ---
genai.configure(api_key=os.getenv("API_KEY"))
model_name = os.getenv("model_name")
model = genai.GenerativeModel(model_name)

# --- CATEGORIAS DE REFERÊNCIA ---
categoria_exemplo = '''
{
  "equipamentos": [
    {"nome": "Guitarra Elétrica", "categoria": "Violão"},
    {"nome": "Baixo Elétrico", "categoria": "Baixo"},
    {"nome": "Teclado Sintetizador", "categoria": "Teclado"},
    {"nome": "Bateria Eletrônica", "categoria": "Bateria"},
    {"nome": "Mesa de Som", "categoria": "Mixagem"},
    {"nome": "Microfone Condensador", "categoria": "Microfone"},
    {"nome": "Amplificador de Guitarra", "categoria": "Processamento de Áudio"},
    {"nome": "Pedal de Efeitos", "categoria": "Processamento de Áudio"},
    {"nome": "Fone de Ouvido Profissional", "categoria": "Fone"},
    {"nome": "Interface de Áudio", "categoria": "Gravação"},
    {"nome": "Controlador MIDI", "categoria": "Produção Musical"},
    {"nome": "Caixa de Som Ativa", "categoria": "Sonorização"},
    {"nome": "Equalizador Gráfico", "categoria": "Processamento de Áudio"},
    {"nome": "Sampler", "categoria": "Processamento de Áudio"},
    {"nome": "Processador de Reverb", "categoria": "Processamento de Áudio"}
  ]
}
'''

try:
    # --- CONEXÃO COM O BANCO DE DADOS ---
    conexao = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    cursor = conexao.cursor(dictionary=True)

    # --- BUSCAR PRODUTOS SEM CATEGORIA ---
    cursor.execute("""
        SELECT p.cod_produto, p.nome AS nome_produto
        FROM produto p
        LEFT JOIN categoria c ON p.cod_produto = c.cod_produto
        WHERE c.nome_categoria IS NULL OR c.nome_categoria = ''
    """)
    produtos_sem_categoria = cursor.fetchall()

    if not produtos_sem_categoria:
        print("Todos os produtos já estão categorizados.")
    else:
        print(f"Classificando {len(produtos_sem_categoria)} produtos...")

        # --- MONTAGEM DA LISTA PARA O PROMPT ---
        lista_produtos = json.dumps(produtos_sem_categoria, ensure_ascii=False)

        # --- PROMPT PARA O GEMINI ---
        prompt = f"""
A seguir, você verá um JSON com uma lista de produtos musicais, contendo o código e o nome do produto.

Sua tarefa é classificar cada item, com base neste conjunto de categorias já existentes:

{categoria_exemplo}

Retorne a lista em formato JSON com o seguinte formato:

[
  {{
    "codigo_produto": "1",
    "nome_produto": "Cabeçote de Amplificador Hi-Gain",
    "categoria": "Processamento de Áudio"
  }},
  ...
]

Caso algum produto não pertença a nenhuma categoria, retorne `"categoria": "Categoria não identificada"`.

JSON com os produtos para classificar:
{lista_produtos}
"""

        # --- CHAMADA À API GEMINI ---
        response = model.generate_content(prompt)
        resultado = response.text.replace(
            "```", "").replace("json", "").strip()
        produtos_classificados = json.loads(resultado)

        # --- ATUALIZAÇÃO NA TABELA CATEGORIA ---
        update_sql = """
        UPDATE categoria
        SET nome_categoria = %s
        WHERE cod_produto = %s
        """

        for p in produtos_classificados:
            categoria = p["categoria"]
            codigo = str(p["codigo_produto"])

            # Se a categoria for "Categoria não identificada", tente novamente
            while categoria == "Categoria não identificada":
                print(
                    f"Produto {codigo} - {p['nome_produto']} -> Categoria não identificada, reclassificando...")

                # Refaça a classificação
                lista_produtos = json.dumps(
                    [{"cod_produto": p["codigo_produto"], "nome_produto": p["nome_produto"]}], ensure_ascii=False)
                prompt = f"""
A seguir, você verá um produto musical, contendo o código e o nome do produto.

Sua tarefa é classificar o item, com base neste conjunto de categorias já existentes:

{categoria_exemplo}

Retorne a lista com o seguinte formato:

[{{"codigo_produto": "{p['codigo_produto']}", "nome_produto": "{p['nome_produto']}", "categoria": "Categoria identificada"}}]

Caso não pertença a nenhuma categoria, retorne `"categoria": "Categoria não identificada"`.
                
JSON com o produto para classificar:
{lista_produtos}
"""
                response = model.generate_content(prompt)
                resultado = response.text.replace(
                    "```", "").replace("json", "").strip()
                p_classificado = json.loads(resultado)[0]
                categoria = p_classificado["categoria"]
                print(f"Produto {codigo} - Reclassificado para: {categoria}")

            cursor.execute(update_sql, (categoria, codigo))
            print(
                f"Produto {codigo} - {p['nome_produto']} -> Categoria atualizada: {categoria}")

        conexao.commit()
        print("Todos os produtos foram atualizados com sucesso!")

except Exception as e:
    print(f"Erro: {e}")

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conexao' in locals() and conexao.is_connected():
        conexao.close()
