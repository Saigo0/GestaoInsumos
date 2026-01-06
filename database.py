import sqlite3

from compra import Compra
from produto import Produto

class Database:
    def __init__(self, db_name="pastelaria.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

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
            FOREIGN KEY (produto_id) REFERENCES produtos (id))''')
        self.conn.commit()

    def salvar_produto(self, nome, unidade_medida):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO produtos (nome, unidade_medida) VALUES (?, ?)", (nome, unidade_medida))
        self.conn.commit()

    def buscar_produtos(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, nome FROM produtos")
        return cursor.fetchall() # Retorna uma lista de tuplas [(1, 'Carne'), (2, 'Farinha')]

    def salvar_compra(self, produto_id, preco, qtd, data):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO compras (produto_id, preco_unitario, quantidade, data)
                          VALUES (?, ?, ?, ?)''', (produto_id, preco, qtd, data))
        self.conn.commit()

    def filtrar_compras_periodo_e_produto(self, mes, ano, produto_id=None):
        cursor = self.conn.cursor()
        filtro_data = f"%/{mes}/{ano}%"
        
        # Base da query
        query = """
            SELECT c.id, p.nome, c.preco_unitario, c.quantidade, c.data 
            FROM compras c
            JOIN produtos p ON c.produto_id = p.id
            WHERE c.data LIKE ?
        """
        params = [filtro_data]

        # Se um produto específico foi selecionado, adicionamos o filtro
        if produto_id:
            query += " AND c.produto_id = ?"
            params.append(produto_id)
        
        query += " ORDER BY c.data DESC"
        
        cursor.execute(query, params)
        return cursor.fetchall()    
    
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