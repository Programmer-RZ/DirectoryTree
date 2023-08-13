from tkinter import *
from tkinter import ttk

from tree import Tree, TextTree, TreeviewTree

class TreeFrame(Frame):
    def __init__(self, master : Misc, tree : Tree) -> None:
        super().__init__(master, bg="darkgrey")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.tree = tree
    
    def update(self) -> None:
        pass

class TextTreeFrame(TreeFrame):
    def __init__(self, master : Misc) -> None:
        super().__init__(master, TextTree())

        self.text : Text = Text(self)
        self.update()
        
        self.text.grid(row=0, column=0, padx=10, pady=10, sticky="EWNS")
    
    def update(self) -> None:
        self.text.config(state=NORMAL)

        self.text.delete(1.0, END)
        for line in self.tree.tree:
            self.text.insert(END, line+"\n")

        self.text.config(state=DISABLED)


class TreeviewTreeFrame(TreeFrame):
    def __init__(self, master : Misc) -> None:
        super().__init__(master, None)

        self.treeview = ttk.Treeview(self)
        
        self.tree = TreeviewTree(self.treeview)

        self.treeview.grid(row=0, column=0, padx=10, pady=10, sticky="EWNS")