class Node:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf      
        self.keys = []              
        self.children = [] 
        # Deleted next and parent cause it's already being supported by Node class keys and children


    # Use this for debugging
    def get_dict(self):
        if self.is_leaf:
            return {
                "keys": self.keys,
                "children": [],
                "is_leaf": True
                }
        return {"keys": self.keys, "children": [child.get_dict() for child in self.children], "is_leaf": False}


class BPlusTree:
    def __init__(self, max_degree):
        self.root = Node(is_leaf=True)
        self.max_degree = max_degree


    # TODO: add function for inserting into parent and leafs as well
    # TODO: add function for inserting into parent and leafs as well
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

        if node == self.root:
        if node == self.root:
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


    def search(self, searchkey):
        node = self.root
        while not node.is_leaf:
            for i, key in enumerate(node.keys):
                if searchkey < key:
                    node = node.children[i]
                    break
            else:
                node = node.children[-1]

        for i, key in enumerate(node.keys):
            if key == searchkey:
                return True
        return False



    # TODO: add function to merge nodes after deletion
    def delete(self):
        pass



    def get_dict(self):
        if self.root == None:
            return {'root': {}}
        return {'root': self.root.get_dict()}


# Add this if __name__ == "__main__" in case you wanted to import this file for graphical view
if __name__ == "__main__":
    tree = BPlusTree(max_degree=4)
    for key in [10, 20, 5, 15, 25, 11, 13, 40, 4, 22, 36, 17]:
        tree.insert(key)
    print(tree.get_dict())
    print()
    print("Root keys:", tree.root.keys)
    for i, child in enumerate(tree.root.children):
        print(f"child{i} keys: {child.keys}")
        for j, childen in enumerate(child.children):
            print(f"child{j} keys: {childen.keys}")

    print(tree.search(1))
    print(tree.search(11))
    