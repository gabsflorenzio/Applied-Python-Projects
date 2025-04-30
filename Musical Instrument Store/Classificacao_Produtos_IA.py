import mysql.connector
import google.generativeai as genai
import json
import os
import time
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


def gerar_conteudo_com_retry(prompt, tentativas=3):
    for tentativa in range(tentativas):
        try:
            response = model.generate_content(prompt)
            return response
        except Exception as e:
            if "429" in str(e):
                print("Limite de requisições atingido. Aguardando 60 segundos...")
                time.sleep(60)
            else:
                print(f"Erro inesperado: {e}")
                raise
    raise RuntimeError("Número máximo de tentativas excedido.")


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

        # --- PREPARA O PROMPT EM LOTE ---
        lista_produtos = json.dumps(produtos_sem_categoria, ensure_ascii=False)

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

        # --- CHAMADA À API COM TRATAMENTO DE ERRO ---
        response = gerar_conteudo_com_retry(prompt)
        resultado = response.text.replace(
            "```", "").replace("json", "").strip()
        produtos_classificados = json.loads(resultado)

        # --- PREPARAR DADOS PARA ATUALIZAÇÃO EM LOTE ---
        updates = []
        ignorados = []

        for p in produtos_classificados:
            categoria = p["categoria"]
            codigo = str(p["codigo_produto"])

            if categoria != "Categoria não identificada":
                updates.append((categoria, codigo))
                print(
                    f"Produto {codigo} - {p['nome_produto']} -> Categoria: {categoria}")
            else:
                ignorados.append((codigo, p["nome_produto"]))
                print(
                    f"Produto {codigo} - {p['nome_produto']} -> Categoria não identificada")

        if updates:
            update_sql = """
            UPDATE categoria
            SET nome_categoria = %s
            WHERE cod_produto = %s
            """
            cursor.executemany(update_sql, updates)
            conexao.commit()
            print(
                f"\n{len(updates)} produtos atualizados com sucesso no banco de dados!")

        if ignorados:
            print(
                f"\n{len(ignorados)} produtos não puderam ser classificados:")
            for cod, nome in ignorados:
                print(f" - {cod}: {nome}")

except Exception as e:
    print(f"Erro: {e}")

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conexao' in locals() and conexao.is_connected():
        conexao.close()
