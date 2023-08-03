import os

class Tree:
    def __init__(self) -> None:

        self.dir : str = os.getcwd()

        # parameters
        self.include_folders = True
        self.include_files = True
        self.include_abspath = False

        self.tree : list = []
        self.depths : list = []
        self.walk : iter = None

        self.divider : str = "     "

        if not os.path.isdir(self.dir):
            raise NotADirectoryError(self.dir)
    
    def save_as(self, path : str):
        with open(path, "w") as file:
            for line in self.tree:
                file.write(line + "\n")
    
    def open(self, path : str):
        with open(path, "r") as file:
            for line in file.readlines():
                self.tree.append("".join(line.split("\n")))

    
    def reset(self) -> None:
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
