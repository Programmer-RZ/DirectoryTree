from tkinter import *
from tkinter import filedialog as fd

from gui.treeframes import TreeFrame, TextTreeFrame

class Tab(Frame):
    def __init__(self, master : Misc, treeframe : TreeFrame, type : str, name : str = "New") -> None:
        super().__init__(master, bg="darkgrey")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.name : str = name
        self.type : str = type

        self.create_tree : Button = Button(self, text="Create directory tree", command=lambda : self.create_popup_window())
        self.create_tree.grid(row=0, column=0, sticky="W", padx=10, pady=5)

        self.treeframe : TreeFrame = treeframe(self)
        self.treeframe.grid(row=1, column=0, sticky="EWNS")

        self.popup : Toplevel = None

    def create_tree_directory(self) -> None:
        pass

    def create_popup_window(self) -> None:
        pass

class TextTreeTab(Tab):
    def __init__(self, master : Misc, name : str = "New") -> None:
        super().__init__(master, TextTreeFrame, "text_tree", name)
        
    
    def create_tree_directory(self) -> None:
        self.treeframe.tree.reset()
        self.treeframe.tree.create_walk()
        self.treeframe.tree.create_tree()
        self.treeframe.update()
    
    def create_popup_window(self) -> None:
        if self.popup and self.popup.winfo_exists():
            return
        
        self.popup = Toplevel(self.master)
        self.popup.title("Create Directory TreeText")
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