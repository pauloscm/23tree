import tkinter as tk
from tkinter import messagebox
import graphviz as gv

class Node:
    # A unique 'name' has to be given to each node to be able to visualize the tree using graphviz
    _name = 0
    def __init__(self, keys=None, children=None):
        self.keys = keys or []
        self.children = children or []
        self.name = Node._name
        Node._name += 1


class TwoThreeTree:
    # Empty tree initialized
    def __init__(self):
        self.root = None

    def insert(self, key):
        # Check if the tree is empty, if it is, create a new node with the key
        if self.root is None:
            self.root = Node(keys=[key])

        # Else, we need to check if the root has children and take care of any splits.
        else:
            new_root, split = self._insert(self.root, key)
            if split:
                prom, left, right = split
                self.root = Node(keys=[prom], children=[left, right])
            else:
                self.root = new_root

    def _insert(self, root, key):
        # This function will return the new root and the split 'values' if there is one
        if not root.children:
            root.keys.append(key)
            root.keys.sort()

            # If the root has three keys, we need to split it and return the split values
            if len(root.keys) > 2:
                prom = root.keys[1]
                left = Node(keys=[root.keys[0]])
                right = Node(keys=[root.keys[2]])
                return None,(prom, left, right)
            else:
                return root, None
        # Else, if the root has children, we need to find the correct child to insert the key into
        else:
            index_children = 0
            while index_children < len(root.keys) and key > root.keys[index_children]:
                index_children += 1
            
            # We use recursion to insert the key into the correct child
            new_child, split = self._insert(root.children[index_children], key)
            if split:
                prom, left, right = split
                # We insert promoted key into current node and we replace the new right and left values
                root.keys.insert(index_children, prom)
                root.children.pop(index_children)
                root.children.insert(index_children, left) 
                root.children.insert(index_children+1, right)

                if len(root.keys) > 2:
                    # If the root has three keys, we need to split it and return the split values
                    mid = root.keys[1]
                    left = Node(keys=[root.keys[0]], children=root.children[:2])
                    right = Node(keys=[root.keys[2]], children=root.children[2:])
                    return None, (mid, left, right)
                else:
                    return root, None 
            # If it doesn't need to be split, we update the child and return  
            else:
                root.children[index_children] = new_child
                return root, None

    def visualize_tree(self, filename="23_tree", filetype="pdf"):
        # Creating tree with graphivz   
        dot = gv.Digraph()

        # If the tree is not empty, we add the nodes and edges.
        if self.root is not None:
            self._add_nodes_edges(dot, self.root)
        
        # Finally, we render the tree
        dot.render(filename, format=filetype, cleanup=True)
    
    def _add_nodes_edges(self, dot, root):
        # Adding the nodes and edges to the graph
        if len(root.keys) == 1:
            dot.node(str(root.name), label=f"{root.keys[0]} | -")
        else:
            dot.node(str(root.name), label=" | ".join(map(str, root.keys)))
        if root.children:
            for child in root.children:

                dot.edge(str(root.name), str(child.name))
                # recursively add the edges for each child
                self._add_nodes_edges(dot, child)
                
class Program:
    def __init__(self):
        self.main = tk.Tk()

        self.label= tk.Label(self.main, text="Enter nodes (space-separated integers):", font=('Helvetica', 14))
        self.label.pack(padx=15, pady=15)

        self.entry = tk.Entry(self.main, font=('Helvetica', 14), width=50)
        self.entry.pack(padx= 15, pady=15)

        self.button = tk.Button(self.main, text="Submit", font=('Helvetica', 14), command=self.create_tree)
        self.button.pack(padx=15, pady=15)

        self.main.mainloop()

    def create_tree(self):
        input_nodes = self.entry.get().strip()

        if not input_nodes:
            messagebox.showerror("Error", "Please enter at least one node.")
            return
        
        try:
            nodes = list(map(int, input_nodes.split()))
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter space-separated integers.")
            return
        
        if len(nodes) != len(set(nodes)):
            nodes = list(set(nodes))
        
        tree = TwoThreeTree()
        for node in nodes:
            tree.insert(int(node))
        tree.visualize_tree()
        self.main.destroy()

program = Program()
