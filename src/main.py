
from tree import Tree
from gui import Window

if __name__ == "__main__":
    tree = Tree()

    window = Window(tree)
    window.mainloop()