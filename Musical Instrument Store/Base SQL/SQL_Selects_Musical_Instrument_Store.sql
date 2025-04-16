-- Selects básicos para conferir os dados
-- Select dos clientes
select * from cliente;
-- Select dos produtos
select * from produto;
-- Select dos vendedores
select * from vendedor;
-- Select das vendas
select * from venda;
-- Select da venda_item
Select * from venda_item;
Select * from categoria;


-- Vizualização do relatório
-- Consulta de Categorias dos produtos
SELECT 
    p.cod_produto,
    p.nome AS nome_produto,
    p.descricao,
    p.preco,
    p.marca,
    p.data_cadastro,
    c.nome_categoria
FROM 
    produto p
JOIN 
    categoria c ON p.cod_produto = c.cod_produto;

-- Consulta de Vendas Detalhadas
SELECT 
    v.cod_venda,
    v.data_venda,
    v.valor_total,
    c.cod_cliente,
    c.nome AS nome_cliente,
    c.cidade AS cidade_cliente,
    c.estado AS estado_cliente,
    vdr.cod_vendedor,
    vdr.nome AS nome_vendedor,
    f.cod_filial,
    f.nome_filial,
    p.cod_produto,
    p.nome AS nome_produto,
    p.categoria AS categoria_produto,
    vi.quantidade,
    vi.preco_unitario,
    (vi.quantidade * vi.preco_unitario) AS total_item
FROM venda v
JOIN cliente c ON v.cod_cliente = c.cod_cliente
LEFT JOIN vendedor vdr ON v.cod_vendedor = vdr.cod_vendedor
JOIN filial f ON v.cod_filial = f.cod_filial
JOIN venda_item vi ON v.cod_venda = vi.cod_venda
JOIN produto p ON vi.cod_produto = p.cod_produto
ORDER BY v.data_venda DESC;


-- Top 10 produtos mais vendidos
SELECT 
    p.cod_produto,
    p.nome AS nome_produto,
    p.categoria,
    SUM(vi.quantidade) AS total_vendido,
    SUM(vi.quantidade * vi.preco_unitario) AS receita_total
FROM venda_item vi
JOIN produto p ON vi.cod_produto = p.cod_produto
GROUP BY p.cod_produto, p.nome, p.categoria
ORDER BY total_vendido DESC
LIMIT 10;

-- Receita por filial
SELECT 
    f.cod_filial,
    f.nome_filial,
    COUNT(DISTINCT v.cod_venda) AS total_vendas,
    SUM(v.valor_total) AS receita_total
FROM venda v
JOIN filial f ON v.cod_filial = f.cod_filial
GROUP BY f.cod_filial, f.nome_filial
ORDER BY receita_total DESC;

-- Venderores com mais vendas - Top 10
SELECT 
    vdr.cod_vendedor,
    vdr.nome AS nome_vendedor,
    COUNT(DISTINCT v.cod_venda) AS total_vendas,
    SUM(v.valor_total) AS receita_total
FROM venda v
JOIN vendedor vdr ON v.cod_vendedor = vdr.cod_vendedor
GROUP BY vdr.cod_vendedor, vdr.nome
ORDER BY receita_total DESC
LIMIT 10;

-- Clientes que mais compraram - Top 10
SELECT 
    c.cod_cliente,
    c.nome AS nome_cliente,
    COUNT(DISTINCT v.cod_venda) AS total_compras,
    SUM(v.valor_total) AS total_gasto
FROM venda v
JOIN cliente c ON v.cod_cliente = c.cod_cliente
GROUP BY c.cod_cliente, c.nome
ORDER BY total_gasto DESC
LIMIT 10;