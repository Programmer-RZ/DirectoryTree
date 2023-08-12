import os

class Tree:
    def __init__(self) -> None:
        self.walk : iter = None
        
        # path of root directory
        self.dir : str = os.getcwd()

        # path of the file
        # when directory tree is saved
        self.path : str = None

    def save(self, newpath : str = None) -> None:
        pass

    def open(self, path : str) -> None:
        pass

    def reset(self) -> None:
        pass

    def create_walk(self) -> None:
        self.walk = os.walk(self.dir)
    
    def create_tree(self) -> None:
        pass


class TextTree(Tree):
    def __init__(self) -> None:
        super().__init__()

        # parameters
        self.include_folders = True
        self.include_files = True
        self.include_abspath = False

        self.tree : list = []
        self.depths : list = []

        self.divider : str = "     "

        if not os.path.isdir(self.dir):
            raise NotADirectoryError(self.dir)
    
    def reset(self) -> None:
        self.tree : list = []
        self.walk : iter = None
    
    def save(self, newpath : str = None) -> None:
        if newpath:
            self.path = newpath
            
        with open(self.path, "w") as file:
            file.write(self.dir + "\n")
            for line in self.tree:
                file.write(line + "\n")
    
    def open(self, path : str) -> None:
        self.path = path
        with open(path, "r") as file:
            self.dir = file.readline().strip("\n")
            for line in file.readlines()[1:]:
                self.tree.append(line.strip("\n"))
    
    def create_walk(self) -> None:
        self.walk = os.walk(self.dir)
    
    def create_tree(self) -> None:

        for folder, subfolders, files in self.walk:
            depth : int = self.get_directory_depth(folder) - self.get_directory_depth(self.dir)
            depth -= 1
            
            # folder
            if self.include_folders:
                path = os.path.abspath(folder)

                if folder != self.dir:
                    if not self.include_abspath:
                        path = self.get_basename(path)

                    self.tree.append(self.divider*(depth) + "|----" + path)
                    self.depths.append(depth)
                    self.add_root_lines(depth)

            # files in folder
            if self.include_files:
                for f in files:
                    try:
                        path = os.path.abspath(f)

                        if not self.include_abspath:
                            path = self.get_basename(path)

                        self.tree.append(self.divider*(depth+1) + "|----" + path)
                        self.depths.append(depth+1)
                    except UnicodeEncodeError:
                        self.tree.append("???")

    def print_tree(self) -> None:
        for line in self.tree:
            print(line)
    
    def get_directory_depth(self, path : str) -> int:
        return path.count(os.path.sep)

    def add_root_lines(self, depth : int) -> None:
        # add | to every directory in self.tree at index depth*5
        for i in range(len(self.tree)-2, 0, -1):
            try:
                if self.tree[i][depth*len(self.divider)] == " " and self.depths[i] >= depth:
                    self.tree[i] = self.tree[i][:depth*len(self.divider)] + "|" + self.tree[i][depth*len(self.divider)+1:]
                else:
                    break
            except IndexError:
                continue
    
    def get_basename(self, path : str) -> str:
        # gets the last part of path
        return os.path.basename(path)
