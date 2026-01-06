import customtkinter as ctk
from datetime import datetime
from tkinter import ttk
from database import Database
from tkinter import messagebox

import customtkinter as ctk
from database import Database

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.db = Database()

        self.produtos_map = {}
        
        self.title("Sistema Villa Sabor - Gestão de Insumos")
        self.geometry("1000x600")

        # Criando abas para organizar o programa
        self.abas = ctk.CTkTabview(self)
        self.abas.pack(padx=20, pady=20, fill="both", expand=True)
        
        self.tab_produto = self.abas.add("Novo Produto")
        self.tab_compra = self.abas.add("Registrar Compra")
        # Adicionar a nova aba
        self.tab_relatorio = self.abas.add("Relatório")
        
        # Dicionário para converter nome do mês em número
        self.meses_map = {
            "Janeiro": "01", "Fevereiro": "02", "Março": "03", "Abril": "04",
            "Maio": "05", "Junho": "06", "Julho": "07", "Agosto": "08",
            "Setembro": "09", "Outubro": "10", "Novembro": "11", "Dezembro": "12"
        }
        
        self.configurar_tela_relatorio()

        self.configurar_tela_produto()
        self.configurar_tela_compra()
        
        # Carregar produtos pela primeira vez
        self.atualizar_menu_produtos()



    def configurar_tela_produto(self):
        # Título dentro da aba
        self.lbl_prod = ctk.CTkLabel(self.tab_produto, text="Cadastro de Insumo", font=("Arial", 20, "bold"))
        self.lbl_prod.pack(pady=15)

        # Entrada do Nome
        self.lbl_nome = ctk.CTkLabel(self.tab_produto, text="Nome do produto:")
        self.lbl_nome.pack()

        self.entry_nome_prod = ctk.CTkEntry(self.tab_produto, placeholder_text="Ex: Farinha de Trigo", width=300)
        self.entry_nome_prod.pack(pady=10)

        # Seleção de Unidade de Medida (Menu Suspenso)
        self.lbl_unidade = ctk.CTkLabel(self.tab_produto, text="Unidade de Medida:")
        self.lbl_unidade.pack()
        
        self.menu_unidade = ctk.CTkOptionMenu(self.tab_produto, values=["kg", "litro", "unidade", "caixa", "pacote"])
        self.menu_unidade.pack(pady=10)

        # Botão de Salvar
        self.btn_salvar_prod = ctk.CTkButton(self.tab_produto, text="Cadastrar Produto", 
                                             command=self.acao_cadastrar_produto,
                                             fg_color="green", hover_color="#006400")
        self.btn_salvar_prod.pack(pady=20)

        # Feedback visual
        self.label_aviso_prod = ctk.CTkLabel(self.tab_produto, text="")
        self.label_aviso_prod.pack()

        self.label_aviso_compra = ctk.CTkLabel(self.tab_compra, text="")
        self.label_aviso_compra.pack()

    def configurar_tela_compra(self):
        self.lbl_titulo = ctk.CTkLabel(self.tab_compra, text="Registrar Nova Compra", font=("Arial", 20, "bold"))
        self.lbl_titulo.pack(pady=(10, 20))

        # --- CAMPO PRODUTO ---
        self.lbl_prod = ctk.CTkLabel(self.tab_compra, text="Selecione o Insumo:", font=("Arial", 12, "bold"))
        self.lbl_prod.pack(padx=20) # anchor="w" alinha o texto à esquerda (West)
        
        self.menu_produtos = ctk.CTkOptionMenu(self.tab_compra, width=300)
        self.menu_produtos.pack(pady=(0, 15), padx=20)

        # --- CAMPO PREÇO ---
        self.lbl_preco = ctk.CTkLabel(self.tab_compra, text="Preço Unitário (R$):", font=("Arial", 12, "bold"))
        self.lbl_preco.pack(padx=20)
        
        self.entry_preco = ctk.CTkEntry(self.tab_compra, placeholder_text="Ex: 5.50", width=300)
        self.entry_preco.pack(pady=(0, 15), padx=20)

        # --- CAMPO QUANTIDADE ---
        self.lbl_qtd = ctk.CTkLabel(self.tab_compra, text="Quantidade Comprada:", font=("Arial", 12, "bold"))
        self.lbl_qtd.pack(padx=20)
        
        self.entry_qtd = ctk.CTkEntry(self.tab_compra, placeholder_text="Ex: 10", width=300)
        self.entry_qtd.pack(pady=(0, 15), padx=20)

        # Botão
        self.btn_salvar = ctk.CTkButton(self.tab_compra, text="Salvar Compra", command=self.acao_registrar_compra)
        self.btn_salvar.pack(pady=20)

    def configurar_tela_relatorio(self):

        agora = datetime.now()
        mes_atual_numero = agora.strftime("%m") # Ex: "01", "05"
        ano_atual = agora.strftime("%Y")        # Ex: "2026"

        # 2. Descobrir o nome do mês a partir do número (usando seu meses_map)
        # Procuramos qual chave (Nome) corresponde ao valor (Número)
        mes_atual_nome = [nome for nome, num in self.meses_map.items() if num == mes_atual_numero][0]

        # Frame para os filtros (fica no topo da aba)
        self.frame_filtros = ctk.CTkFrame(self.tab_relatorio)
        self.frame_filtros.pack(pady=10, padx=10, fill="x")

        # 3. Configurar os menus com os valores atuais como padrão
        self.menu_mes = ctk.CTkOptionMenu(self.frame_filtros, values=list(self.meses_map.keys()))
        self.menu_mes.set(mes_atual_nome) # <--- Define o mês atual
        self.menu_mes.pack(side="left", padx=5, pady=5)

        ano_int = int(datetime.now().year)
        lista_anos = [str(ano_int - 1), str(ano_int), str(ano_int + 1), str(ano_int + 2)]
        self.menu_ano = ctk.CTkOptionMenu(self.frame_filtros, values=lista_anos)
        self.menu_ano.set(ano_atual)      # <--- Define o ano atual
        self.menu_ano.pack(side="left", padx=5, pady=5)

        self.btn_filtrar = ctk.CTkButton(self.frame_filtros, text="Filtrar", command=self.gerar_relatorio)
        self.btn_filtrar.pack(side="left", padx=5, pady=5)

        # Configuração da Tabela (Treeview)
        # Nota: O Treeview é do Tkinter padrão, então a estilização é um pouco diferente
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", borderwidth=0)
        style.map("Treeview", background=[('selected', '#1f538d')])

        self.tabela = ttk.Treeview(self.tab_relatorio, 
                           columns=("id", "prod", "preco", "qtd", "total", "data"), 
                           show="headings")

        # 2. Configure os cabeçalhos (Headings)
        self.tabela.heading("id", text="ID") # Esse texto não aparecerá se a largura for 0
        self.tabela.heading("prod", text="Produto")
        self.tabela.heading("preco", text="Preço Unit.")
        self.tabela.heading("qtd", text="Qtd")
        self.tabela.heading("total", text="Total")
        self.tabela.heading("data", text="Data")

        # 3. O PULO DO GATO: Esconder a coluna do ID
        # Definimos a largura como 0 e proibimos o redimensionamento (stretch=False)
        self.tabela.column("id", width=0, stretch=ctk.NO)
        self.tabela.column("qtd", width=50)
        self.tabela.column("total", width=100)
        
        self.tabela.pack(pady=10, padx=10, fill="both", expand=True)

        # Label para o Gasto Total
        self.lbl_total_geral = ctk.CTkLabel(self.tab_relatorio, text="Gasto Total: R$ 0,00", font=("Arial", 18, "bold"))
        self.lbl_total_geral.pack(pady=10) 

        self.btn_excluir = ctk.CTkButton(self.tab_relatorio, text="Excluir Compra Selecionada", 
                                     command=self.acao_excluir_compra,
                                     fg_color="#8B0000")
        self.btn_excluir.pack(pady=10)  

        self.gerar_relatorio() 

    def atualizar_menu_produtos(self):
        """Busca produtos no banco e atualiza o OptionMenu"""
        dados = self.db.buscar_produtos()
        
        # Limpa e preenche o dicionário {Nome: ID}
        self.produtos_map = {nome: id_prod for id_prod, nome in dados}
        
        # Se houver produtos, atualiza o menu suspenso
        nomes = list(self.produtos_map.keys())
        if nomes:
            self.menu_produtos.configure(values=nomes)
            self.menu_produtos.set(nomes[0]) # Define o primeiro como padrão
        else:
            self.menu_produtos.configure(values=["Cadastre um produto primeiro"])

    def acao_registrar_compra(self):
        nome_selecionado = self.menu_produtos.get()
        produto_id = self.produtos_map.get(nome_selecionado)
        
        if not produto_id:
            print("Erro: Produto não selecionado")
            return

        try:
            preco = float(self.entry_preco.get().replace(',', '.'))
            qtd = float(self.entry_qtd.get().replace(',', '.'))
            data = datetime.now().strftime("%d/%m/%Y %H:%M")

            self.db.salvar_compra(produto_id, preco, qtd, data)
            self.label_aviso_compra.configure(text=f"✅ {nome_selecionado} cadastrado com sucesso!", text_color="green")
            
            # Limpar campos
            self.entry_preco.delete(0, 'end')
            self.entry_qtd.delete(0, 'end')
            
        except ValueError:
            print("Erro: Insira valores numéricos válidos!")    

    def gerar_relatorio(self):
        # Limpar tabela atual
        for i in self.tabela.get_children():
            self.tabela.delete(i)

        

        # Obter valores dos filtros
        mes_nome = self.menu_mes.get()
        mes_num = self.meses_map[mes_nome]
        ano = self.menu_ano.get()

        # Buscar no banco
        compras_do_mes = self.db.filtrar_compras_por_periodo(mes_num, ano)
        
        gasto_total_mes = 0

        for r in compras_do_mes:
            # r[0]=id, r[1]=nome, r[2]=preco, r[3]=qtd, r[4]=data
            preco = r[2]
            qtd = r[3]
            total_item = preco * qtd
            gasto_total_mes += total_item
            
            # Inserir na tabela
            self.tabela.insert("", "end", values=(
                r[0],
                r[1], 
                f"R$ {preco:.2f}", 
                qtd, 
                f"R$ {total_item:.2f}", 
                r[4]
            ))

        # Atualizar o Label de Total
        self.lbl_total_geral.configure(text=f"Gasto Total no Mês: R$ {gasto_total_mes:.2f}")
        
    def acao_cadastrar_produto(self):
        nome = self.entry_nome_prod.get().strip()
        unidade = self.menu_unidade.get()

        if nome:
            try:
                self.db.salvar_produto(nome, unidade)
                self.label_aviso_prod.configure(text=f"✅ {nome} cadastrado com sucesso!", text_color="green")
                self.entry_nome_prod.delete(0, 'end') # Limpa o campo
                self.atualizar_menu_produtos()
            except Exception as e:
                self.label_aviso_prod.configure(text=f"❌ Erro ao salvar: {e}", text_color="red")
        else:
            self.label_aviso_prod.configure(text="⚠️ Digite o nome do produto!", text_color="orange")

    def acao_excluir_compra(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            return

        item_valores = self.tabela.item(selecionado, "values")
        compra_id = item_valores[0] 
        
        # DEBUG: Veja no terminal se o ID que aparece aqui é um número correto
        print(f"DEBUG: Tentando excluir a compra com ID: {compra_id}")

        confirmar = messagebox.askyesno("Confirmação", "Deseja excluir?")
        if confirmar:
            self.db.excluir_compra(compra_id)
            self.gerar_relatorio() # Isso é fundamental para atualizar a tela!


if __name__ == "__main__":
    app = App()
    app.mainloop()