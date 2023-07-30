from tkinter import *
from tkinter import filedialog as fd

from tree import Tree

class GUI(Tk):
    def __init__(self, tree : Tree):
        super().__init__()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title("Directory Tree")
        self.geometry("1000x600")

        self.tree_frame = TreeFrame(self, tree)
        self.tree_frame.grid(row=0, column=0, padx=10, pady=10, sticky="EWNS")

        self.sidepanel = Sidepanel(self, self.tree_frame)
        self.sidepanel.grid(row=0, column=1, padx=10, pady=10, sticky="EWNS")


class TreeFrame(Frame):
    def __init__(self, master : Misc, tree : Tree):
        super().__init__(master, bg="darkgrey")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.tree : Tree = tree

        self.text : Text = Text(self)
        self.update_text()
        
        self.text.grid(row=0, column=0, padx=10, pady=10, sticky="EWNS")
    
    def update_text(self):
        self.text.config(state=NORMAL)

        self.text.delete(1.0, END)
        for line in self.tree.tree:
            self.text.insert(END, line+"\n")

        self.text.config(state=DISABLED)


class Sidepanel(Frame):
    def __init__(self, master : Misc, treeframe : TreeFrame):
        super().__init__(master, bg="darkgrey")

        self.treeframe : TreeFrame = treeframe

        self.pick_directory : Button = Button(self, text="Choose directory", command=lambda : self.choose_directory())
        self.pick_directory.grid(row=0, column=0, padx=10, pady=10)

        self.create_tree : Button = Button(self, text="Create directory tree", command=lambda : self.create_directory_tree())
        self.create_tree.grid(row=1, column=0, padx=10, pady=10)
    
    def create_directory_tree(self):
        self.treeframe.tree.reset()
        self.treeframe.tree.create_walk()
        self.treeframe.tree.create_tree()
        self.treeframe.update_text()
    
    def choose_directory(self):
        self.treeframe.tree.dir = fd.askdirectory()
        