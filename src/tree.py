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
    
    def reset(self):
        self.walk = None
        self.tree = []
    
    def create_walk(self) -> None:
        self.walk = os.walk(self.dir)
    
    def create_tree(self) -> None:
        root_path = os.path.abspath(self.dir)

        for folder, subfolders, files in self.walk:
            depth : int = self.get_directory_depth(folder) - self.get_directory_depth(self.dir)
            depth -= 1
            
            # folder
            if self.include_folders:
                path = os.path.abspath(folder)

                if path != root_path:
                    if not self.include_abspath:
                        path = self.getDifference(path, root_path)

                    self.tree.append(self.divider*(depth) + "├----" + path)
                    self.depths.append(depth)
                    self.addRootLines(depth)

            # files in folder
            if self.include_files:
                for f in files:
                    try:
                        path = os.path.abspath(f)

                        if not self.include_abspath:
                            path = self.getDifference(path, root_path)

                        self.tree.append(self.divider*(depth+1) + "├----" + path)
                        self.depths.append(depth+1)
                    except UnicodeEncodeError:
                        self.tree.append("???")
                
                self.addRootLines(depth+1)

    def print_tree(self) -> None:
        for line in self.tree:
            print(line)
    
    def get_directory_depth(self, path : str) -> int:
        return path.count(os.path.sep)

    def addRootLines(self, depth : int) -> None:
        # add | to every directory in self.tree at index depth*5
        for i in range(len(self.tree)-2, 0, -1):
            try:
                if self.tree[i][depth*len(self.divider)] == " " and self.depths[i] >= depth:
                    self.tree[i] = self.tree[i][:depth*len(self.divider)] + "│" + self.tree[i][depth*len(self.divider)+1:]
                else:
                    break
            except IndexError:
                continue
    
    def getDifference(self, full_path, reference_path):
        # gets the remaining path of full_path - reference_path
        full_path = os.path.normpath(full_path)
        reference_path = os.path.normpath(reference_path)

        # Check if the reference_path is a prefix of the full_path
        if not full_path.startswith(reference_path):
            raise ValueError("The reference_path is not a prefix of the full_path")

        # Extract the remaining part of the full_path
        remaining_path = full_path[len(reference_path):].strip(os.path.sep)

        return remaining_path
