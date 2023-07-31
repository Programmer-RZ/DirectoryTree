import os

class Tree:
    def __init__(self) -> None:

        self.dir : str = os.getcwd()

        # parameters
        self.include_folders = True
        self.include_files = True
        self.include_abspath = False

        self.tree : list = []
        self.walk : iter = None

        self.divider : str = "     "

        if not os.path.isdir(self.dir):
            raise NotADirectoryError(self.dir)
    
    def reset(self):
        self.walk = None
        self.tree = []
    
    def create_walk(self) -> None:
        self.walk = os.walk(self.dir)
    
    def create_tree(self) -> None:

        for folder, subfolders, files in self.walk:
            depth : int = self.get_directory_depth(folder) - self.get_directory_depth(self.dir)
            depth -= 1
            
            # folder
            if self.include_folders:
                if folder != self.dir:
                    self.tree.append(self.divider*(depth) + "├----" + folder)
                    self.addRootLines(depth)

            # files in folder
            if self.include_files:
                for f in files:
                    try:
                        self.tree.append(self.divider*(depth+1) + "├----" + f)
                    except UnicodeEncodeError:
                        self.tree.append("???")

    def print_tree(self) -> None:
        for line in self.tree:
            print(line)
    
    def get_directory_depth(self, path : str) -> int:
        return path.count(os.path.sep)

    def addRootLines(self, depth : int) -> None:
        # add | to every directory in self.tree at index depth*5
        for i in range(len(self.tree)):
            try:
                if self.tree[i][depth*len(self.divider)] == " ":
                    self.tree[i] = self.tree[i][:depth*len(self.divider)] + "│" + self.tree[i][depth*len(self.divider)+1:]
            except IndexError:
                continue