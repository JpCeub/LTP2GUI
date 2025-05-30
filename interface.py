import tkinter as tk
from tkinter import ttk, messagebox
import bancoBigBOM

def iniciar_interface():
    root = tk.Tk()
    root.title("Mercadinho Big Bom - O mais brabo")

    # Nome do Mercadinho
    titulo_label = tk.Label(root, text="Mercadinho Big Bom⚡", font=("Arial", 18, "bold"))
    titulo_label.pack(pady=10)

    # Frame principal
    frame_principal = tk.Frame(root)
    frame_principal.pack(padx=10, pady=10, fill="both", expand=True)

    # Frame das Prateleiras 
    frame_prateleiras = tk.LabelFrame(frame_principal, text="Prateleiras")
    frame_prateleiras.pack(fill="x", pady=5)

    tk.Label(frame_prateleiras, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_prateleira = tk.Entry(frame_prateleiras)
    entry_prateleira.grid(row=0, column=1, padx=5, pady=5)

    tk.Button(frame_prateleiras, text="Adicionar", command=lambda: adicionar_prateleira()).grid(row=0, column=2, padx=5)
    tk.Button(frame_prateleiras, text="Atualizar", command=lambda: atualizar_prateleira_selecionada()).grid(row=0, column=3, padx=5)
    tk.Button(frame_prateleiras, text="Excluir", command=lambda: deletar_prateleira_selecionada()).grid(row=0, column=4, padx=5)
    tk.Button(frame_prateleiras, text="Especificar Produtos", command=lambda: mostrar_produtos_prateleira()).grid(row=0, column=5, padx=5)

    tree_prateleiras = ttk.Treeview(frame_prateleiras, columns=("ID", "Nome"), show="headings")
    tree_prateleiras.heading("ID", text="ID")
    tree_prateleiras.heading("Nome", text="Nome")
    tree_prateleiras.grid(row=1, column=0, columnspan=6, padx=5, pady=5, sticky="ew")

    # Frame dos Produtos
    frame_produtos = tk.LabelFrame(frame_principal, text="Produtos")
    frame_produtos.pack(fill="x", pady=10)

    tk.Label(frame_produtos, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_produto = tk.Entry(frame_produtos)
    entry_produto.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_produtos, text="Preço:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
    entry_preco = tk.Entry(frame_produtos)
    entry_preco.grid(row=0, column=3, padx=5, pady=5)

    tk.Label(frame_produtos, text="Prateleira:").grid(row=0, column=4, padx=5, pady=5, sticky="e")
    prateleira_var = tk.StringVar()
    menu_prateleira = ttk.OptionMenu(frame_produtos, prateleira_var, "")
    menu_prateleira.grid(row=0, column=5, padx=5, pady=5)

    tk.Button(frame_produtos, text="Adicionar Produto", command=lambda: adicionar_produto()).grid(row=1, column=0, columnspan=2, pady=5)
    tk.Button(frame_produtos, text="Atualizar Produto", command=lambda: atualizar_produto_selecionado()).grid(row=1, column=2, columnspan=2, pady=5)
    tk.Button(frame_produtos, text="Excluir Produto", command=lambda: deletar_selecionado()).grid(row=1, column=4, columnspan=2, pady=5)

    tree = ttk.Treeview(frame_principal, columns=("ID", "Nome", "Preco", "Prateleira"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("Preco", text="Preço")
    tree.heading("Prateleira", text="Prateleira")
    tree.pack(fill="both", expand=True, padx=5, pady=5)

    # Funções internas
    def atualizar_lista_prateleiras():
        menu_prateleira['menu'].delete(0, 'end')
        nomes = []
        for _, nome in bancoBigBOM.listar_prateleiras():
            nomes.append(nome)
            menu_prateleira['menu'].add_command(label=nome, command=tk._setit(prateleira_var, nome))
        if nomes:
            prateleira_var.set(nomes[0])

    def atualizar_tabela_prateleiras():
        tree_prateleiras.delete(*tree_prateleiras.get_children())
        for id_, nome in bancoBigBOM.listar_prateleiras():
            tree_prateleiras.insert("", tk.END, values=(id_, nome))

    def atualizar_lista_produtos():
        tree.delete(*tree.get_children())
        for item in bancoBigBOM.listar_produtos():
            tree.insert("", tk.END, values=item)

    def mostrar_produtos_prateleira():
        item = tree_prateleiras.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione uma prateleira.")
            return
        prateleira_nome = tree_prateleiras.item(item)['values'][1]
        tree.delete(*tree.get_children())
        for produto in bancoBigBOM.listar_produtos():
            if produto[3] == prateleira_nome:
                tree.insert("", tk.END, values=produto)

    def adicionar_prateleira():
        nome = entry_prateleira.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Informe o nome da prateleira.")
            return
        try:
            bancoBigBOM.inserir_prateleira(nome)
            atualizar_lista_prateleiras()
            atualizar_tabela_prateleiras()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def atualizar_prateleira_selecionada():
        item = tree_prateleiras.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione uma prateleira para atualizar.")
            return
        try:
            prateleira_id = tree_prateleiras.item(item)['values'][0]
            novo_nome = entry_prateleira.get().strip()
            bancoBigBOM.atualizar_prateleira(prateleira_id, novo_nome)
            atualizar_lista_prateleiras()
            atualizar_tabela_prateleiras()
            atualizar_lista_produtos()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def deletar_prateleira_selecionada():
        item = tree_prateleiras.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione uma prateleira para excluir.")
            return
        resposta = messagebox.askyesno("Confirmação", "Tem certeza que quer excluir esta prateleira?")
        if not resposta:
            return
        try:
            prateleira_id = tree_prateleiras.item(item)['values'][0]
            bancoBigBOM.deletar_prateleira(prateleira_id)
            atualizar_lista_prateleiras()
            atualizar_tabela_prateleiras()
            atualizar_lista_produtos()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def adicionar_produto():
        nome = entry_produto.get().strip()
        preco = entry_preco.get().strip()
        prateleira_nome = prateleira_var.get()
        if not nome or not preco:
            messagebox.showwarning("Aviso", "Digite um nome e um preço.")
            return
        try:
            preco = float(preco)
            bancoBigBOM.inserir_produto(nome, preco, prateleira_nome)
            atualizar_lista_produtos()
        except ValueError:
            messagebox.showerror("Erro", "Preço deve ser um número.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def atualizar_produto_selecionado():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um produto para atualizar.")
            return
        try:
            produto_id = tree.item(item)['values'][0]
            novo_nome = entry_produto.get().strip()
            novo_preco = float(entry_preco.get())
            nova_prateleira = prateleira_var.get()
            bancoBigBOM.atualizar_produto(produto_id, novo_nome, novo_preco, nova_prateleira)
            atualizar_lista_produtos()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def deletar_selecionado():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um produto para excluir.")
            return
        resposta = messagebox.askyesno("Confirmação", "Tem certeza que quer excluir este produto?")
        if not resposta:
            return
        produto_id = tree.item(item)['values'][0]
        bancoBigBOM.deletar_produto(produto_id)
        atualizar_lista_produtos()

    # Inicializações
    atualizar_lista_prateleiras()
    atualizar_tabela_prateleiras()
    atualizar_lista_produtos()
    root.mainloop()
