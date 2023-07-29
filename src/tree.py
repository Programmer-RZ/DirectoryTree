import os

class Tree:
    def __init__(self, dir):
        self.dir : str = dir
        self.tree : list = []

        if not os.path.isdir(self.dir):
            raise NotADirectoryError(self.dir)
    
    def create_tree(self):

        for folder, subfolders, files in os.walk(self.dir):
            depth = self.get_directory_depth(folder) - self.get_directory_depth(self.dir)
            depth -= 1

            if folder == self.dir:
                continue
            
            # folder
            self.tree.append("     "*(depth) + "|----" + folder)
            self.addRootLines(depth)

            # files in folder
            for f in files:
                try:
                    #self.tree.append("     "*(depth+1) + "|")
                    self.tree.append("     "*(depth+1) + "|----" + f)
                except UnicodeEncodeError:
                    self.tree.append("???")

    def print_tree(self):
        for line in self.tree:
            print(line)
    
    def get_directory_depth(self, path):
        return path.count(os.path.sep)

    def addRootLines(self, depth):
        # add | to every directory in self.tree at index depth*5
        for i in range(len(self.tree)):
            try:
                if self.tree[i][depth*5] == " ":
                    self.tree[i] = self.tree[i][:depth*5] + "|" + self.tree[i][depth*5+1:]
            except IndexError:
                continue