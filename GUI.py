import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import pydot
from networkx.drawing.nx_pydot import graphviz_layout


class BPlusTreeVisualizer(ctk.CTk):
    def __init__(self, tree):
        super().__init__()
        self.tree = tree
        self.title("B+ Tree")
        self.geometry("1200x800")
        self.setup_ui()

    def setup_ui(self):
        self.inp = ctk.CTkFrame(self, fg_color="black", bg_color="black")
        self.inp.pack(fill="x")

        self.input_frame = ctk.CTkFrame(self.inp, fg_color="black")
        self.input_frame.pack()

        self.input_label = ctk.CTkLabel(self.input_frame, text="key", text_color="black")
        self.input_label.pack(side="left", pady=50, padx=5)

        self.input_entry = ctk.CTkEntry(self.input_frame, width=40)
        self.input_entry.pack(side="left", padx=5)

        self.insert_button = ctk.CTkButton(self.input_frame, text="Insert", command=self.insert_key, width=80, fg_color="gainsboro", text_color="black", hover_color="white", font=("Roboto", 14))
        self.insert_button.pack(side="left", padx=5)

        self.delete_button = ctk.CTkButton(self.input_frame, text="Delete", command=self.delete_key, width=80, fg_color="gainsboro", text_color="black", hover_color="white", font=("Roboto", 14))
        self.delete_button.pack(side="left", padx=5)

        self.search_label = ctk.CTkLabel(self.input_frame, text="Search")
        self.search_label.pack(side="left", padx=5)

        self.search_entry = ctk.CTkEntry(self.input_frame, width=40)
        self.search_entry.pack(side="left", padx=5)

        self.search_button = ctk.CTkButton(self.input_frame, text="Search", command=self.search_key, width=80, fg_color="gainsboro", text_color="black", hover_color="white", font=("Roboto", 14))
        self.search_button.pack(side="left", padx=5)


        self.clear_label = ctk.CTkLabel(self.input_frame, text="clear", text_color="black")
        self.clear_label.pack(side="left", pady=50, padx=5)

        self.clear_button = ctk.CTkButton(self.input_frame, text="clear", command=self.clear_tree, width=80, fg_color="gainsboro", text_color="black", hover_color="white", font=("Roboto", 14))
        self.clear_button.pack(side="left", padx=5)


        self.max_label = ctk.CTkLabel(self.input_frame, text="max keys", width=40)
        self.max_label.pack(side="left", padx=5)

        self.max_dropdown = ctk.CTkOptionMenu(
            self.input_frame,
            values=["3", "4", "5", "6", "7"],
            command=self.set_max_keys,
            fg_color="gainsboro",
            button_color="gray",
            text_color="black"
        )
        self.max_dropdown.set("3")
        self.max_dropdown.pack(side="left", padx=5)


        self.canvas_frame = ctk.CTkFrame(self)
        self.canvas_frame.pack(fill="both", expand=True)

        self.note_label = ctk.CTkLabel(self.canvas_frame, text_color="black",text='', bg_color="white", height=30)
        self.note_label.pack(side="top",fill="both", pady=0)

        self.figure = Figure(figsize=(5, 5))
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.canvas_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

        self.update_visualization()


    def insert_key(self):
        try:
            key = int(self.input_entry.get())
            self.tree.insert(key)
            self.update_visualization()
            print("\n-------------------tree------------------")
            self.tree.print_tree2()
            self.note_label.configure(text=f"")

        except:
            print("invalid key")
            self.note_label.configure(text=f"invalid key")

        self.input_entry.delete("0", "end")



    def delete_key(self):
        try:
            key = int(self.input_entry.get())
            self.tree.delete(key)
            result = self.tree.delete(key)
            self.update_visualization()
            print("\n-------------------tree------------------")
            self.tree.print_tree2()
            self.note_label.configure(text=f"")

        except:
            self.note_label.configure(text=f"Key not found in the tree.")

        self.input_entry.delete("0", "end")



    def search_key(self):
        key = int(self.search_entry.get())
        result = self.tree.search(key)
        self.search_entry.delete("0", "end")
        print(f"Search result for {key}: {result}") 
        self.note_label.configure(text=f"serach result for {key}: {result}")
        

        

    def set_max_keys(self, selected_value):
        max_keys = int(selected_value)
        self.tree.max_degree = max_keys
        self.tree.clear()
        print(f"Max keys set to: {max_keys}")
        self.update_visualization()



    def clear_tree(self):
        self.tree.clear()
        self.update_visualization()
        print("Tree has been cleared.")



    def update_visualization(self):
        self.ax.clear()

        G = nx.DiGraph()
        if self.tree.root:  # اطمینان از اینکه ریشه درخت None نیست
            self.build_graph(G, self.tree.root)

        pos = graphviz_layout(G, prog="dot")
        
        nx.draw(
            G,
            pos,
            ax=self.ax,
            with_labels=True,
            labels=nx.get_node_attributes(G, 'label'),  # استفاده از برچسب‌ها
            node_size=1000,
            font_size=10,
            node_color='white',
            font_weight='bold',
            edge_color='gray',
            font_color='black'
        )
        self.canvas.draw()



    def build_graph(self, G, node, parent=None, node_id_map=None, counter=None):
        if node_id_map is None:
            node_id_map = {}
        if counter is None:
            counter = [0]  # شمارنده برای تولید شناسه یکتا

        if node not in node_id_map:
            node_id = f"Node_{counter[0]}"
            node_id_map[node] = node_id
            counter[0] += 1
        else:
            node_id = node_id_map[node]

        G.add_node(node_id, label=str(node.keys))

        if parent:
            G.add_edge(parent, node_id)

        if not node.is_leaf:
            for child in node.children:
                self.build_graph(G, child, node_id, node_id_map, counter)


def start_visualizer(tree):
    app = BPlusTreeVisualizer(tree)
    app.mainloop()
