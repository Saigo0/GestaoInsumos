class Compra:
    def __init__(self, id_compra, produto, preco_unitario, quantidade, data):
        self.id = id_compra
        self.produto = produto # Objeto da classe Produto
        self.preco_unitario = preco_unitario
        self.quantidade = quantidade
        self.data = data
    
    @property
    def valor_total(self):
        return self.preco_unitario * self.quantidade
        