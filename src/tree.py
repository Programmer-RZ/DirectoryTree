import os

class Tree:
    def __init__(self):
        self.dir : str = ".."
        self.tree : list = os.walk(self.dir)
    
    def print_tree(self):
        print("\n")

        for folder, subfolders, files in self.tree:
            depth = self.get_directory_depth(folder) - self.get_directory_depth(self.dir)

            print("|" + "----"*(depth) + folder)

            print("|")

            for f in files:
                print("|" + "----"*(depth+1) + f)

            print("|")

        print("\n")
    
    def get_directory_depth(self, path):
        return path.count(os.path.sep)