from tkinter import *
from tkinter import filedialog as fd
import os

# fix blurred text
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

from gui.tabs import Tab, TextTreeTab, TreeviewTreeTab

from gui.custom.tabcontrol import CustomNotebook

class Window(Tk):
    def __init__(self) -> None:
        super().__init__()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #self.geometry("1000x600")
        self.state('zoomed')

        self.tab_control : CustomNotebook = CustomNotebook(self)

        self.menubar : Menubar = Menubar(self, self.tab_control)

        self.tab_control.grid(row=0, column=0, padx=5, pady=5, sticky="EWNS")
        
        self.title(f"Directory Tree")
        self.config(menu=self.menubar)



class Menubar(Menu):
    def __init__(self, master : Misc, tabcontrol : CustomNotebook):
        super().__init__(master)

        self.tabcontrol : CustomNotebook = tabcontrol

        filemenu : Menu = Menu(self, tearoff=0)

        filemenu.add_command(label="New text tree", command=lambda : self.new_texttree_tab())
        filemenu.add_command(label="New treeview tree", command=lambda : self.new_treeviewtree_tab())

        filemenu.add_separator()

        filemenu.add_command(label="Save as", command=lambda : self.save_as())
        filemenu.add_command(label="Save", command=lambda : self.save())

        filemenu.add_separator()

        filemenu.add_command(label="Open text tree", command=lambda : self.open_texttree())

        self.add_cascade(label="File", menu=filemenu)
    
    def new_texttree_tab(self) -> None:
        new = TextTreeTab(self.master)
        self.tabcontrol.add(new, text=new.name)
        self.tabcontrol.select(self.tabcontrol.index("end")-1)
    
    def new_treeviewtree_tab(self) -> None:
        new = TreeviewTreeTab(self.master)
        self.tabcontrol.add(new, text=new.name)
        self.tabcontrol.select(self.tabcontrol.index("end")-1)
    
    def open_texttree(self) -> None:
        filetypes = (("Text files", "*.txt"),)
        file = fd.askopenfilename(filetypes=filetypes)

        if not file:
            return

        new : TextTreeTab = TextTreeTab(self.master, os.path.splitext(os.path.basename(file))[0])
        new.treeframe.tree.open(file)
        new.treeframe.update()
        
        self.tabcontrol.add(new, text=new.name)
    
    def save_as(self) -> None:
        selected_tab : Tab = self.tabcontrol.nametowidget(self.tabcontrol.select())

        if selected_tab.type == "text_tree":
            filetypes = (("Text files", "*.txt"),)

        path = fd.asksaveasfilename(defaultextension="*.*", filetypes=filetypes)

        if not path:
            return

        selected_tab.name = os.path.splitext(os.path.basename(path))[0]
        selected_tab.treeframe.tree.save(path)

        self.tabcontrol.tab(selected_tab, text=selected_tab.name)
    
    def save(self) -> None:
        selected_tab : Tab = self.tabcontrol.nametowidget(self.tabcontrol.select())

        if not selected_tab.treeframe.tree.path or not os.path.isfile(selected_tab.treeframe.tree.path):
            self.save_as()

        else:
            selected_tab.treeframe.tree.save()

        