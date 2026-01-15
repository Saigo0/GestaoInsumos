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
        
        # 1. Primeiro cria todas as telas
        self.configurar_tela_relatorio()
        self.configurar_tela_produto()
        self.configurar_tela_compra()
        
        # 2. Depois carrega os dados iniciais em todas elas
        self.atualizar_menu_produtos()           # Popula aba de compra
        self.atualizar_menu_produtos_relatorio() # Popula aba de relatório
        self.atualizar_filtros_fornecedor()      # Popula fornecedores



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

        self.lbl_fornecedor = ctk.CTkLabel(self.tab_compra, text="Fornecedor:", font=("Arial", 12, "bold"))
        self.lbl_fornecedor.pack(padx=20)

        self.entry_fornecedor = ctk.CTkEntry(self.tab_compra, placeholder_text="Ex: Atacadão S.A.", width=300)
        self.entry_fornecedor.pack(pady=(0, 15), padx=20)

        # Botão
        self.btn_salvar = ctk.CTkButton(self.tab_compra, text="Salvar Compra", command=self.acao_registrar_compra)
        self.btn_salvar.pack(pady=20)

    def atualizar_menu_fornecedores(self):
        lista = ["Todos"] + self.db.buscar_fornecedores_unicos()
        self.menu_filtro_fornecedor.configure(values=lista)

    def configurar_tela_relatorio(self):

        agora = datetime.now()
        mes_atual_numero = agora.strftime("%m")
        ano_atual = agora.strftime("%Y")
        mes_atual_nome = [nome for nome, num in self.meses_map.items() if num == mes_atual_numero][0]

        # Frame Principal dos Filtros
        self.frame_filtros = ctk.CTkFrame(self.tab_relatorio)
        self.frame_filtros.pack(pady=10, padx=10, fill="x")

        # --- FILTRO MÊS ---
        self.container_mes = ctk.CTkFrame(self.frame_filtros, fg_color="transparent")
        self.container_mes.pack(side="left", padx=10, pady=5)
        
        ctk.CTkLabel(self.container_mes, text="Mês:", font=("Arial", 11, "bold")).pack()
        self.menu_mes = ctk.CTkOptionMenu(self.container_mes, values=list(self.meses_map.keys()), width=120)
        self.menu_mes.set(mes_atual_nome)
        self.menu_mes.pack()

        # --- FILTRO ANO ---
        self.container_ano = ctk.CTkFrame(self.frame_filtros, fg_color="transparent")
        self.container_ano.pack(side="left", padx=10, pady=5)
        
        ctk.CTkLabel(self.container_ano, text="Ano:", font=("Arial", 11, "bold")).pack()
        ano_int = int(datetime.now().year)
        lista_anos = [str(ano_int - 1), str(ano_int), str(ano_int + 1), str(ano_int + 2)]
        self.menu_ano = ctk.CTkOptionMenu(self.container_ano, values=lista_anos, width=80)
        self.menu_ano.set(ano_atual)
        self.menu_ano.pack()

        # --- FILTRO PRODUTO ---
        self.container_prod = ctk.CTkFrame(self.frame_filtros, fg_color="transparent")
        self.container_prod.pack(side="left", padx=10, pady=5)
        
        ctk.CTkLabel(self.container_prod, text="Produto:", font=("Arial", 11, "bold")).pack()
        self.menu_filtro_produto = ctk.CTkOptionMenu(self.container_prod, values=["Todos"], width=150)
        self.menu_filtro_produto.pack()

        # --- FILTRO FORNECEDOR ---
        self.container_forn = ctk.CTkFrame(self.frame_filtros, fg_color="transparent")
        self.container_forn.pack(side="left", padx=10, pady=5)
        
        ctk.CTkLabel(self.container_forn, text="Fornecedor:", font=("Arial", 11, "bold")).pack()
        self.menu_filtro_fornecedor = ctk.CTkOptionMenu(self.container_forn, values=["Todos"], width=150)
        self.menu_filtro_fornecedor.pack()

        # Botão Filtrar (centralizado verticalmente em relação aos outros)
        self.btn_filtrar = ctk.CTkButton(self.frame_filtros, text="🔍 Filtrar", command=self.gerar_relatorio, width=100)
        self.btn_filtrar.pack(side="left", padx=20, pady=(20, 0)) # pady maior em cima para alinhar com os menus

        # Configuração da Tabela (Treeview)
        # Nota: O Treeview é do Tkinter padrão, então a estilização é um pouco diferente
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", borderwidth=0)
        style.map("Treeview", background=[('selected', '#1f538d')])

        # 1. ATUALIZAÇÃO: Adicione "fornecedor" na lista de colunas
        self.tabela = ttk.Treeview(self.tab_relatorio, 
                           columns=("id", "prod", "preco", "qtd", "total", "data", "fornecedor"), 
                           show="headings")

        # 2. Configure os cabeçalhos (incluindo o fornecedor)
        self.tabela.heading("id", text="ID")
        self.tabela.heading("prod", text="Produto")
        self.tabela.heading("preco", text="Preço Unit.")
        self.tabela.heading("qtd", text="Qtd")
        self.tabela.heading("total", text="Total")
        self.tabela.heading("data", text="Data")
        self.tabela.heading("fornecedor", text="Fornecedor") # <-- Adicionado

        # 3. Ajuste de larguras
        self.tabela.column("id", width=0, stretch=ctk.NO)
        self.tabela.column("qtd", width=50)
        self.tabela.column("total", width=100)
        self.tabela.column("fornecedor", width=150) # <-- Adicionado
        
        self.tabela.pack(pady=10, padx=10, fill="both", expand=True)

        self.lbl_total_geral = ctk.CTkLabel(self.tab_relatorio, text="Gasto Total: R$ 0,00", font=("Arial", 18, "bold"))
        self.lbl_total_geral.pack(pady=5) 

        # --- FRAME PARA BOTÕES DE AÇÃO ---
        # Criar um frame para os botões ficarem lado a lado
        self.frame_botoes_acao = ctk.CTkFrame(self.tab_relatorio, fg_color="transparent")
        self.frame_botoes_acao.pack(pady=10)

        # AGORA SIM: Criando o botão de EDITAR
        self.btn_editar = ctk.CTkButton(self.frame_botoes_acao, text="Editar Selecionado", 
                                        command=self.acao_editar_compra,
                                        fg_color="orange", hover_color="#CC7722", text_color="black")
        self.btn_editar.pack(side="left", padx=10)

        self.btn_excluir = ctk.CTkButton(self.frame_botoes_acao, text="Excluir Selecionada", 
                                         command=self.acao_excluir_compra,
                                         fg_color="#8B0000")
        self.btn_excluir.pack(side="left", padx=10)

        self.gerar_relatorio() 
    
    def acao_editar_compra(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma compra para editar.")
            return

        valores = self.tabela.item(selecionado, "values")
        # Desempacotando agora com o fornecedor incluído (são 7 valores)
        id_c, prod_nome, preco, qtd, total, data, forn_atual = valores 

        janela_edit = ctk.CTkToplevel(self)
        janela_edit.title(f"Editando: {prod_nome}")
        janela_edit.geometry("400x450")
        janela_edit.grab_set()
        janela_edit.attributes("-topmost", True) # Garante que a janela fique na frente

        ctk.CTkLabel(janela_edit, text=f"Editando {prod_nome}", font=("Arial", 16, "bold")).pack(pady=10)
        
        ctk.CTkLabel(janela_edit, text="Preço Unitário:").pack()
        ent_preco = ctk.CTkEntry(janela_edit)
        ent_preco.insert(0, preco.replace("R$ ", "")) 
        ent_preco.pack(pady=5)

        ctk.CTkLabel(janela_edit, text="Quantidade:").pack()
        ent_qtd = ctk.CTkEntry(janela_edit)
        ent_qtd.insert(0, qtd)
        ent_qtd.pack(pady=5)

        ctk.CTkLabel(janela_edit, text="Fornecedor:").pack()
        ent_forn = ctk.CTkEntry(janela_edit)
        ent_forn.insert(0, forn_atual if forn_atual != "Não inf." else "")
        ent_forn.pack(pady=5)

        def salvar_alteracoes():
            try:
                novo_p = float(ent_preco.get().replace(',', '.'))
                nova_q = float(ent_qtd.get().replace(',', '.'))
                novo_f = ent_forn.get().strip()

                self.db.editar_compra(id_c, novo_p, nova_q, novo_f)
                janela_edit.destroy()
                self.gerar_relatorio()
                self.atualizar_filtros_fornecedor() # Atualiza o filtro se o nome mudar
                messagebox.showinfo("Sucesso", "Registro atualizado!")
            except ValueError:
                messagebox.showerror("Erro", "Valores de preço ou quantidade inválidos.")

        ctk.CTkButton(janela_edit, text="Salvar Alterações", command=salvar_alteracoes, fg_color="green").pack(pady=20)

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

    def atualizar_menu_produtos_relatorio(self):
        dados = self.db.buscar_produtos()
        print(f"DEBUG Relatório: Produtos encontrados no banco: {dados}") # Veja se aparece algo no terminal
        
        nomes = ["Todos"] + [nome for id_prod, nome in dados]
        self.menu_filtro_produto.configure(values=nomes)
        
        # Se o que estava selecionado sumiu, volta para "Todos"
        if self.menu_filtro_produto.get() not in nomes:
            self.menu_filtro_produto.set("Todos")

    def gerar_relatorio(self):
        # 1. Limpa a tabela
        for i in self.tabela.get_children():
            self.tabela.delete(i)

        # 2. Captura os valores dos filtros da tela
        mes_nome = self.menu_mes.get()
        mes_num = self.meses_map[mes_nome]
        ano = self.menu_ano.get()
        
        # Filtro de Produto
        prod_nome = self.menu_filtro_produto.get()
        id_produto = self.produtos_map.get(prod_nome) if prod_nome != "Todos" else None
        
        # Filtro de Fornecedor
        fornecedor_selecionado = self.menu_filtro_fornecedor.get()

        # 3. Busca no banco com todos os filtros
        dados = self.db.filtrar_compras_completo(mes_num, ano, id_produto, fornecedor_selecionado)

        total_financeiro = 0

        # 4. Preenche a tabela
        for r in dados:
            # r[0]=id, r[1]=nome, r[2]=preco, r[3]=qtd, r[4]=data, r[5]=fornecedor
            valor_total_item = r[2] * r[3]
            total_financeiro += valor_total_item
            
            # Lembre-se que a coluna ID [0] está oculta, então os dados começam no index 1
            self.tabela.insert("", "end", values=(
                r[0], 
                r[1], 
                f"R$ {r[2]:.2f}", 
                r[3], 
                f"R$ {valor_total_item:.2f}", 
                r[4],
                r[5] if r[5] else "Não inf." # Trata se o fornecedor for vazio
            ))

        # 5. Atualiza o label de total no rodapé
        self.lbl_total_geral.configure(text=f"Total Geral: R$ {total_financeiro:.2f}")

    def atualizar_filtros_fornecedor(self):
        lista_db = self.db.listar_fornecedores_unicos()
        opcoes = ["Todos"] + sorted(lista_db)
        self.menu_filtro_fornecedor.configure(values=opcoes)    
    
    def acao_cadastrar_produto(self):
        nome = self.entry_nome_prod.get().strip()
        unidade = self.menu_unidade.get()

        if nome:
            try:
                self.db.salvar_produto(nome, unidade)
                self.label_aviso_prod.configure(text=f"✅ {nome} cadastrado com sucesso!", text_color="green")
                self.entry_nome_prod.delete(0, 'end') # Limpa o campo
                self.atualizar_menu_produtos()           # Atualiza aba de Compra
                self.atualizar_menu_produtos_relatorio()
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