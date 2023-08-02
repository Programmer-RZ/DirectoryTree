from tkinter import *
from tkinter import filedialog as fd

from tree import Tree
from custom.tabcontrol import CustomNotebook

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


class TreeFrame(Frame):
    def __init__(self, master : Misc) -> None:
        super().__init__(master, bg="darkgrey")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.tree : Tree = Tree()

        self.text : Text = Text(self)
        self.update_text()
        
        self.text.grid(row=0, column=0, padx=10, pady=10, sticky="EWNS")
    
    def update_text(self) -> None:
        self.text.config(state=NORMAL)

        self.text.delete(1.0, END)
        for line in self.tree.tree:
            self.text.insert(END, line+"\n")

        self.text.config(state=DISABLED)


class GUI(Frame):
    def __init__(self, master : Misc) -> None:
        super().__init__(master, bg="darkgrey")
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.treeframe : TreeFrame = TreeFrame(self)
        self.treeframe.grid(row=1, column=0, sticky="EWNS")

        self.create_tree : Button = Button(self, text="Create directory tree", command=lambda : self.create_popup_window())
        self.create_tree.grid(row=0, column=0, sticky="W", padx=10)

        self.popup : Toplevel = None
        
    
    def create_tree_directory(self) -> None:
        self.treeframe.tree.reset()
        self.treeframe.tree.create_walk()
        self.treeframe.tree.create_tree()
        self.treeframe.update_text()
    
    def create_popup_window(self) -> None:
        if self.popup and self.popup.winfo_exists():
            return
        
        self.popup = Toplevel(self.master)
        self.popup.title("Create Directory Tree")
        self.popup.grab_set()

        # directory
        current_directory : Label = Label(self.popup, width=40, text=self.treeframe.tree.dir, borderwidth=2, relief="ridge")
        current_directory.grid(row=0, column=0, padx=10, pady=10)

        pick_directory : Button = Button(self.popup, text="Browse", command=lambda : choose_directory())
        pick_directory.grid(row=0, column=1, padx=10, pady=10)

        # parameters
        folders_string_var : StringVar = StringVar(value="on")
        folders : Checkbutton = Checkbutton(self.popup, text="Include folders", variable=folders_string_var, onvalue="on", offvalue="off")
        folders.grid(row=1, column=0)

        files_string_var : StringVar = StringVar(value="on")
        files : Checkbutton = Checkbutton(self.popup, text="Include files", variable=files_string_var, onvalue="on", offvalue="off")
        files.grid(row=2, column=0, pady=10)

        abspath_string_var : StringVar = StringVar(value="off")
        abspath : Checkbutton = Checkbutton(self.popup, text="Include absolute path", variable=abspath_string_var, onvalue="on", offvalue="off")
        abspath.grid(row=3, column=0)

        # confirm
        confirm : Button = Button(self.popup, text="Confirm", command=lambda : confirm())
        confirm.grid(row=4, column=2, padx=5, pady=10, sticky="ES")

        def choose_directory() -> None:
            dir : str = fd.askdirectory()
            if dir:
                self.treeframe.tree.dir = dir
                current_directory.config(text=dir)
                self.winfo_toplevel().title(f"Directory Tree - {dir}")
        
        def confirm() -> None:
            if folders_string_var.get() == "on":
                self.treeframe.tree.include_folders = True
            else:
                self.treeframe.tree.include_folders = False
            
            if files_string_var.get() == "on":
                self.treeframe.tree.include_files = True
            else:
                self.treeframe.tree.include_files = False
            
            if abspath_string_var.get() == "on":
                self.treeframe.tree.include_abspath = True
            else:
                self.treeframe.tree.include_abspath = False

            self.create_tree_directory()
            
            self.popup.destroy()
            self.popup = None


class Menubar(Menu):
    def __init__(self, master : Misc, tabcontrol : CustomNotebook):
        super().__init__(master)

        self.tabcontrol : CustomNotebook = tabcontrol

        filemenu : Menu = Menu(self, tearoff=0)
        filemenu.add_command(label="New", command=lambda : self.new_gui())
        filemenu.add_separator()
        filemenu.add_command(label="Save as", command=lambda : self.save_as())

        self.add_cascade(label="File", menu=filemenu)
    
    def new_gui(self) -> None:
        new = GUI(self.master)
        self.tabcontrol.add(new, text=f"New {len(self.tabcontrol.tabs())+1}")
    
    def save_as(self) -> None:
        filetypes = (("Text files", "*.txt"),)
        path = fd.asksaveasfilename(defaultextension="*.*", filetypes=filetypes)

        selected_tab : GUI = self.tabcontrol.nametowidget(self.tabcontrol.select())
        selected_tab.treeframe.tree.save_as(path)

        