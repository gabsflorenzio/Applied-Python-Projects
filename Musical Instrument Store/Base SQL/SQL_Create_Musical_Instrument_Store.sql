CREATE DATABASE faker_test_2;
USE faker_test_2;


-- Criar tabela de produtos
CREATE TABLE produto (
    cod_produto INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10,2) NOT NULL,
    marca VARCHAR(100),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar tabela das filiais das empresas
CREATE TABLE filial (
    cod_filial INT AUTO_INCREMENT PRIMARY KEY,
    nome_filial VARCHAR(255) NOT NULL,
    cnpj VARCHAR(18) UNIQUE NOT NULL,
    endereco VARCHAR(255) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    estado CHAR(2) NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(150) UNIQUE,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar tabela dos vendedores
CREATE TABLE vendedor (
    cod_vendedor INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(150) UNIQUE,
    cod_filial INT NOT NULL,
    data_admissao DATE NOT NULL,
    salario DECIMAL(10,2) NOT NULL,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cod_filial) REFERENCES filial(cod_filial) ON DELETE CASCADE
);

-- Criar a tabela dos clientes
CREATE TABLE cliente (
    cod_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    data_nascimento DATE,
    genero ENUM('Masculino', 'Feminino', 'Outro', 'Prefiro não informar'),
    telefone VARCHAR(20),
    email VARCHAR(150) UNIQUE,
    endereco VARCHAR(255),
    complemento VARCHAR(100),
    bairro VARCHAR(100),
    cidade VARCHAR(100) NOT NULL,
    estado CHAR(2) NOT NULL,
    cep VARCHAR(10),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar a tabela de vendas
CREATE TABLE venda (
    cod_venda INT AUTO_INCREMENT PRIMARY KEY,
    cod_cliente INT NOT NULL,
    cod_vendedor INT,  -- Agora pode ser NULL
    cod_filial INT NOT NULL,
    data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valor_total DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (cod_cliente) REFERENCES cliente(cod_cliente) ON DELETE CASCADE,
    FOREIGN KEY (cod_vendedor) REFERENCES vendedor(cod_vendedor) ON DELETE SET NULL,
    FOREIGN KEY (cod_filial) REFERENCES filial(cod_filial) ON DELETE CASCADE
);

-- Criar a tabela de Venda_Item
CREATE TABLE venda_item (
    cod_venda INT NOT NULL,
    cod_produto INT NOT NULL,
    quantidade INT NOT NULL CHECK (quantidade > 0),
    preco_unitario DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (cod_venda, cod_produto),
    FOREIGN KEY (cod_venda) REFERENCES venda(cod_venda) ON DELETE CASCADE,
    FOREIGN KEY (cod_produto) REFERENCES produto(cod_produto) ON DELETE CASCADE
);

-- Criar a tabela de Categoria
 CREATE TABLE categoria (
    cod_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);