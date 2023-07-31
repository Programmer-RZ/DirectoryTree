from tkinter import *
from tkinter import filedialog as fd

from tree import Tree

class Window(Tk):
    def __init__(self, tree : Tree):
        super().__init__()

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.geometry("1000x600")

        self.tree_frame = TreeFrame(self, tree)
        self.tree_frame.grid(row=1, column=0, sticky="EWNS")

        self.gui = GUI(self, self.tree_frame)
        self.gui.grid(row=0, column=0, sticky="EWNS")

        self.title(f"Directory Tree - {self.tree_frame.tree.dir}")


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


class GUI(Frame):
    def __init__(self, master : Misc, treeframe : TreeFrame):
        super().__init__(master, bg="darkgrey")

        self.treeframe : TreeFrame = treeframe

        self.create_tree : Button = Button(self, text="Create directory tree", command=lambda : self.create_popup_window())
        self.create_tree.grid(row=0, column=0, padx=10, pady=10)


        self.popup : Toplevel = None
        
    
    def create_tree_directory(self):
        self.treeframe.tree.reset()
        self.treeframe.tree.create_walk()
        self.treeframe.tree.create_tree()
        self.treeframe.update_text()
    
    def create_popup_window(self):
        if self.popup and self.popup.winfo_exists():
            return
        
        self.popup = Toplevel(self.master)
        self.popup.title("Create Directory Tree")
        self.popup.grab_set()

        # directory
        current_directory : Label = Label(self.popup, text=self.treeframe.tree.dir, borderwidth=2, relief="ridge")
        current_directory.grid(row=0, column=0, padx=10, pady=10)

        pick_directory : Button = Button(self.popup, text="Browse", command=lambda : choose_directory())
        pick_directory.grid(row=0, column=1, padx=10, pady=10)

        # confirm
        confirm : Button = Button(self.popup, text="Confirm", command=lambda : confirm())
        confirm.grid(row=1, column=1, padx=5, pady=10)

        # cancel
        cancel : Button = Button(self.popup, text="Cancel", command=lambda : cancel())
        cancel.grid(row=1, column=3, padx=5, pady=10)

        def choose_directory():
            dir : str = fd.askdirectory()
            if dir:
                self.treeframe.tree.dir = dir
                current_directory.config(text=dir)
                self.winfo_toplevel().title(f"Directory Tree - {dir}")
        
        def confirm():
            self.create_tree_directory()
            
            self.popup.destroy()
            self.popup = None
        
        def cancel():
            self.popup.destroy()
            self.popup = None

        