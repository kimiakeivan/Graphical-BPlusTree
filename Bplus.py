class Node:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf      # is this node a leaf?
        self.keys = []              # for keys
        self.children = []          #for internal nodes
        self.next = None            #for leaves
        self.parent = None          #for parents



class BPlusTree:
    def __init__(self, max_degree):
        self.root = Node(is_leaf=True)
        self.max_degree = max_degree


    
    def insert(self, key):
        leaf = self.find_leaf(self.root, key)
        leaf.keys.append(key)
        leaf.keys.sort()

        if len(leaf.keys) >= self.max_degree:
            self.split(leaf)



    def find_leaf(self, node, key):
        if node.is_leaf:
            return node
        for i, item in enumerate(node.keys):
            if key < item:
                return self.find_leaf(node.children[i], key)            
        return self.find_leaf(node.children[-1], key)



    def split(self, node):
        mid_index = len(node.keys) // 2
        mid_key = node.keys[mid_index]
        new_node = Node(is_leaf=node.is_leaf)
        new_node.keys = node.keys[mid_index:]
        node.keys = node.keys[:mid_index]

        if not node.is_leaf:
            new_node.children =node.children[mid_index:]
            node.children = node.children[:mid_index]

        if node==self.root:
            new_root = Node()
            new_root.keys = [mid_key]
            new_root.children = [node, new_node]
            self.root = new_root
        else:
            parent = self.find_parent(self.root, node)
            parent.keys.append(mid_key)
            parent.keys.sort()
            parent.children.insert(parent.keys.index(mid_key)+1, new_node)
            if len(parent.keys) >= self.max_degree:
                self.split(parent)


    
    def find_parent(self, node, child):
        if node.is_leaf:
            return None

        for i, child_node in enumerate(node.children):

            if child_node==child:
                return node
            parent = self.find_parent(child_node, child)
            if parent:
                return parent
        return None




    def delete(self):
        pass




    def search(self):
        pass

    
    
tree = BPlusTree(max_degree=4)
tree.insert(10)
tree.insert(20)
tree.insert(5)
tree.insert(15)
tree.insert(25)
tree.insert(11)
tree.insert(13)


print("Root keys:", tree.root.keys)
print("Child 1 keys:", tree.root.children[0].keys)
print("Child 2 keys:", tree.root.children[1].keys)
print("Child 2 keys:", tree.root.children[2].keys)