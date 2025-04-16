# 🎵 Musical Instrument Store

Projeto de gerenciamento de dados de uma loja de instrumentos musicais com foco em automação, banco de dados relacional e uso de inteligência artificial generativa para classificação de produtos.

---

## 🎯 Objetivo

Criar um sistema que simula a base de dados de uma loja de instrumentos musicais, utilizando dados gerados com o pacote `faker`, armazenando em um banco **MySQL** e integrando com **IA generativa (Google Gemini)** para classificar os produtos automaticamente com base em suas descrições e características.

---

## 🧱 Tecnologias utilizadas

| Tecnologia | Função |
|------------|--------|
| `Python 3.10+` | Linguagem base |
| `mysql.connector` | Conexão com MySQL |
| `Faker` | Geração de dados falsos e realistas |
| `dotenv` | Carregamento seguro de variáveis de ambiente |
| `os` | Interação com sistema |
| `pandas` | Manipulação de dados e visualização |
| `json` | Exportação de dados estruturados |
| `google.generativeai` | Classificação automática com IA (Gemini) |

---

## 📘 Etapas do projeto

### 1. 🔧 Configuração do banco de dados (MySQL)

O script `db_setup.py` realiza:

- Criação do banco `musical_store`
- Criação de tabela `products` com os seguintes campos:
  - `id`
  - `name`
  - `brand`
  - `price`
  - `description`
  - `stock_quantity`
  - `category` (preenchido posteriormente via IA)

> As credenciais do banco são armazenadas no arquivo `.env` para segurança.

---

### 2. 🎲 Geração de dados fake com `Faker`

O script `data_generator.py` gera centenas de produtos falsos com dados como:

- Nome do instrumento (ex: "Violino acústico premium")
- Marca (ex: "Yamaha", "Fender")
- Preço (em R$)
- Descrição (frases simulando o texto de vendas)
- Quantidade em estoque

Esses dados são enviados ao banco pelo script `insert_data.py`.

---

### 3. 🧠 Classificação de produtos com IA (Gemini)

O script `classify_products.py` utiliza a IA do Google Gemini para **analisar a descrição dos produtos** e atribuir automaticamente uma **categoria** ao produto, como por exemplo:

- Cordas
- Percussão
- Teclas
- Sopros
- Acessórios

> A IA recebe os dados brutos e responde com a categoria mais apropriada para cada instrumento.

---

## 🔐 Arquivo `.env` (exemplo)

```dotenv
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=musical_store

GOOGLE_API_KEY=sua_chave_api
