import sqlite3

# Conecta ao banco (se não existir, ele cria o arquivo automaticamente)
conexao = sqlite3.connect('pastelaria.db')
cursor = conexao.cursor()

# Criar tabela de Produtos
cursor.execute('''
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
)
''')

# Criar tabela de Compras
cursor.execute('''
CREATE TABLE IF NOT EXISTS compras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER,
    data DATE,
    quantidade REAL,
    valor_pago REAL,
    FOREIGN KEY (produto_id) REFERENCES produtos (id)
)
''')

conexao.commit()
conexao.close()
print("Banco de dados configurado com sucesso!")