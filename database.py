import sqlite3

from compra import Compra
from produto import Produto

class Database:
    def __init__(self, db_name="pastelaria.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
        self.atualizar_estrutura()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            unidade_medida TEXT NOT NULL)''')
        self.conn.commit()

        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS compras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER,
            preco_unitario REAL NOT NULL,
            quantidade REAL NOT NULL,
            data TEXT NOT NULL,
            fornecedor TEXT, 
            FOREIGN KEY (produto_id) REFERENCES produtos (id)
        )''')
        self.conn.commit()

    def salvar_produto(self, nome, unidade_medida):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO produtos (nome, unidade_medida) VALUES (?, ?)", (nome, unidade_medida))
        self.conn.commit()

    def buscar_produtos(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, nome FROM produtos")
        return cursor.fetchall() # Retorna uma lista de tuplas [(1, 'Carne'), (2, 'Farinha')]

    def salvar_compra(self, produto_id, preco, qtd, data, fornecedor):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO compras (produto_id, preco_unitario, quantidade, data, fornecedor)
                          VALUES (?, ?, ?, ?, ?)''', (produto_id, preco, qtd, data, fornecedor))
        self.conn.commit()

    def editar_compra(self, compra_id, preco, qtd, fornecedor):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE compras 
            SET preco_unitario = ?, quantidade = ?, fornecedor = ?
            WHERE id = ?
        """, (preco, qtd, fornecedor, compra_id))
        self.conn.commit()

    def buscar_fornecedores_unicos(self):
        """Busca todos os fornecedores cadastrados para preencher o filtro"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT fornecedor FROM compras WHERE fornecedor IS NOT NULL")
        return [row[0] for row in cursor.fetchall()]

    def filtrar_compras_completo(self, mes, ano, produto_id=None, fornecedor=None):
        cursor = self.conn.cursor()
        
        # Filtro base por Mês/Ano
        filtro_data = f"%/{mes}/{ano}%"
        
        query = """
            SELECT c.id, p.nome, c.preco_unitario, c.quantidade, c.data, c.fornecedor 
            FROM compras c
            JOIN produtos p ON c.produto_id = p.id
            WHERE c.data LIKE ?
        """
        params = [filtro_data]

        # Adiciona filtro de Produto se não for "Todos"
        if produto_id:
            query += " AND c.produto_id = ?"
            params.append(produto_id)

        # Adiciona filtro de Fornecedor se não for "Todos"
        if fornecedor and fornecedor != "Todos":
            query += " AND c.fornecedor = ?"
            params.append(fornecedor)

        query += " ORDER BY c.data DESC"
        
        cursor.execute(query, params)
        return cursor.fetchall()    
    
    def listar_fornecedores_unicos(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT fornecedor FROM compras WHERE fornecedor IS NOT NULL AND fornecedor != ''")
        retorno = cursor.fetchall()
        return [f[0] for f in retorno]
    
    def atualizar_estrutura(self):
        cursor = self.conn.cursor()
        try:
            # Tentamos adicionar a coluna. 
            # Se ela já existir, o SQLite vai dar um erro e o 'except' vai segurar.
            cursor.execute("ALTER TABLE compras ADD COLUMN fornecedor TEXT")
            self.conn.commit()
            print("Coluna 'fornecedor' adicionada com sucesso!")
        except sqlite3.OperationalError:
            # Se cair aqui, é porque a coluna já existe. Não fazemos nada.
            print("A coluna 'fornecedor' já existe. Pulando migração.")
    
    def excluir_compra(self, compra_id):
        cursor = self.conn.cursor()
        # Verifique se o nome da tabela e da coluna ID estão corretos
        cursor.execute("DELETE FROM compras WHERE id = ?", (compra_id,))
        self.conn.commit() # <--- ESSA LINHA É OBRIGATÓRIA
        print(f"Banco: Comando de exclusão enviado para o ID {compra_id}")

    def excluir_produto(self, produto_id):
        """
        Aviso: Se você excluir um produto que já tem compras registradas,
        o banco pode impedir ou deixar 'compras órfãs' dependendo da configuração.
        """
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
        self.conn.commit()

    def listar_todas(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM compras")
        rows = cursor.fetchall() # Retorna uma lista de tuplas
        
        # Transformando as tuplas do SQL em uma lista de objetos 'Compra'
        compras_objetos = []
        for r in rows:
            p = Produto(None, r[1])
            c = Compra(r[0], p, r[3], r[2])
            compras_objetos.append(c)
        return compras_objetos