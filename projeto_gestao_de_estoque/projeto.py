import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import sqlite3
import ttkbootstrap as tb


class InventoryManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestão de Estoque")
        self.root.geometry("900x700")

        self.style = tb.Style("litera")

        self.connection = sqlite3.connect("estoque.db")
        self.cursor = self.connection.cursor()
        self.create_tables()

        self.control_frame = ttk.Frame(self.root, padding=10)
        self.control_frame.pack(fill=tk.X)

        self.tree_frame = ttk.Frame(self.root)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)

        self.history_frame = ttk.Frame(self.root, padding=10)
        self.history_frame.pack(fill=tk.BOTH, expand=True)

        self.add_button = ttk.Button(self.control_frame, text="Adicionar Produto", command=self.add_product)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = ttk.Button(self.control_frame, text="Editar Produto", command=self.edit_product)
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.remove_button = ttk.Button(self.control_frame, text="Remover Produto", command=self.remove_product)
        self.remove_button.pack(side=tk.LEFT, padx=5)

        self.tree = ttk.Treeview(self.tree_frame, columns=("Nome", "Preço", "Quantidade"), show="headings", height=15)
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Preço", text="Preço")
        self.tree.heading("Quantidade", text="Quantidade")
        self.tree.column("Nome", width=300)
        self.tree.column("Preço", width=100)
        self.tree.column("Quantidade", width=100)
        self.tree.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.total_value = 0
        self.total_label = ttk.Label(
            self.root, text=f"Valor Total do Estoque: R$ {self.total_value:.2f}",
            font=("Helvetica", 14, "bold"), padding=10
        )
        self.total_label.pack(anchor=tk.E)

        self.history_tree = ttk.Treeview(
            self.history_frame,
            columns=("Nome", "Preço", "Quantidade", "Tipo", "Data e Hora"),
            show="headings", height=10
        )
        self.history_tree.heading("Nome", text="Nome")
        self.history_tree.heading("Preço", text="Preço")
        self.history_tree.heading("Quantidade", text="Quantidade")
        self.history_tree.heading("Tipo", text="Tipo")
        self.history_tree.heading("Data e Hora", text="Data e Hora")
        self.history_tree.column("Nome", width=200)
        self.history_tree.column("Preço", width=100)
        self.history_tree.column("Quantidade", width=100)
        self.history_tree.column("Tipo", width=100)
        self.history_tree.column("Data e Hora", width=200)
        self.history_tree.pack(fill=tk.BOTH, expand=True)

        history_scrollbar = ttk.Scrollbar(self.history_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscroll=history_scrollbar.set)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.load_data()
        self.load_history()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS estoque (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco REAL NOT NULL,
                quantidade INTEGER NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS historico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco REAL NOT NULL,
                quantidade INTEGER NOT NULL,
                tipo TEXT NOT NULL,
                data_hora TEXT NOT NULL
            )
        """)
        self.connection.commit()

    def load_data(self):
        self.cursor.execute("SELECT nome, preco, quantidade FROM estoque")
        rows = self.cursor.fetchall()
        for row in rows:
            self.tree.insert("", tk.END, values=row)
            self.total_value += row[1] * row[2]
            self.update_total_label()

    def load_history(self):
        self.cursor.execute("SELECT nome, preco, quantidade, tipo, data_hora FROM historico")
        rows = self.cursor.fetchall()
        for row in rows:
            self.history_tree.insert("", tk.END, values=row)

    def update_total_label(self):
        self.total_label.config(text=f"Valor Total do Estoque: R$ {self.total_value:.2f}")

    def add_product(self):
        nome = simpledialog.askstring("Adicionar Produto", "Nome do produto:")
        if not nome:
            return
        try:
            preco = simpledialog.askfloat("Adicionar Produto", "Preço do produto:")
            quantidade = simpledialog.askinteger("Adicionar Produto", "Quantidade do produto:", minvalue=1)
        except (ValueError, TypeError):
            messagebox.showerror("Erro", "Entrada inválida.")
            return

        self.tree.insert("", tk.END, values=(nome, preco, quantidade))
        self.total_value += preco * quantidade
        self.update_total_label()

        self.cursor.execute("INSERT INTO estoque (nome, preco, quantidade) VALUES (?, ?, ?)", (nome, preco, quantidade))
        self.cursor.execute(
            "INSERT INTO historico (nome, preco, quantidade, tipo, data_hora) VALUES (?, ?, ?, ?, ?)",
            (nome, preco, quantidade, "Entrada", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
        self.connection.commit()
        self.history_tree.insert("", tk.END, values=(nome, preco, quantidade, "Entrada", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")

    def edit_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Atenção", "Nenhum produto selecionado para edição.")
            return

        produto = self.tree.item(selected_item)["values"]
        nome_produto, preco_atual, quantidade_atual = produto[0], float(produto[1]), int(produto[2])

        novo_preco = simpledialog.askfloat("Editar Produto", "Novo preço do produto:", initialvalue=preco_atual)
        if novo_preco is None:
            return
        nova_quantidade = simpledialog.askinteger("Editar Produto", "Nova quantidade do produto:", initialvalue=quantidade_atual)
        if nova_quantidade is None:
            return

        quantidade_diferenca = nova_quantidade - quantidade_atual
        tipo_movimentacao = "Entrada" if quantidade_diferenca > 0 else "Saída"

        self.tree.item(selected_item, values=(nome_produto, novo_preco, nova_quantidade))

        self.total_value -= preco_atual * quantidade_atual
        self.total_value += novo_preco * nova_quantidade
        self.update_total_label()

        self.cursor.execute("UPDATE estoque SET preco = ?, quantidade = ? WHERE nome = ?", (novo_preco, nova_quantidade, nome_produto))
        self.cursor.execute(
            "INSERT INTO historico (nome, preco, quantidade, tipo, data_hora) VALUES (?, ?, ?, ?, ?)",
            (nome_produto, novo_preco, abs(quantidade_diferenca), tipo_movimentacao, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
        self.connection.commit()

        self.history_tree.insert(
            "", tk.END, values=(nome_produto, novo_preco, abs(quantidade_diferenca), tipo_movimentacao, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )

        messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")

    def remove_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Atenção", "Nenhum produto selecionado para remoção.")
            return

        produto = self.tree.item(selected_item)["values"]
        nome_produto, preco, quantidade = produto[0], float(produto[1]), int(produto[2])

        quantidade_remover = simpledialog.askinteger(
            "Remover Produto",
            f"Quantidade disponível: {quantidade}\nQuanto deseja remover?",
            minvalue=1,
            maxvalue=quantidade
        )
        if quantidade_remover is None:
            return

        nova_quantidade = quantidade - quantidade_remover
        if nova_quantidade > 0:
            self.tree.item(selected_item, values=(nome_produto, preco, nova_quantidade))
        else:
            self.tree.delete(selected_item)

        self.total_value -= preco * quantidade_remover
        self.update_total_label()

        self.cursor.execute("UPDATE estoque SET quantidade = ? WHERE nome = ?", (nova_quantidade, nome_produto))
        if nova_quantidade == 0:
            self.cursor.execute("DELETE FROM estoque WHERE nome = ?", (nome_produto,))
        self.cursor.execute(
            "INSERT INTO historico (nome, preco, quantidade, tipo, data_hora) VALUES (?, ?, ?, ?, ?)",
            (nome_produto, preco, quantidade_remover, "Saída", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
        self.connection.commit()

        self.history_tree.insert(
            "", tk.END, values=(nome_produto, preco, quantidade_remover, "Saída", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )

        messagebox.showinfo("Sucesso", "Produto removido com sucesso!")


if __name__ == "__main__":
    root = tb.Window(themename="litera")
    app = InventoryManager(root)
    root.mainloop()
