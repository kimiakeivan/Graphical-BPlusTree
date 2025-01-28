class Node:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf      
        self.keys = []              
        self.children = [] 
        self.next = None

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
            del new_node.keys[0]
            new_node.children =node.children[mid_index+1:]
            node.children = node.children[:mid_index+1]

        #add pointer to point to the next nodwe
        if node.is_leaf:
            new_node.next = node.next
            node.next = new_node


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


    def print_tree(self, node=None, level=0):
        if node is None:
            node = self.root
        if node is None:
            return
        print("Level", level, ":", node.keys)
        if not node.is_leaf:
            for child in node.children:
                self.print_tree(child, level + 1)
            

    def print_tree2(self):
            if not self.root:
                print("Tree is empty.")
                return 
            queue = [(self.root, 0)]
            current_level = -1
            level_nodes = []
            while queue:
                node, level = queue.pop(0)
                if level != current_level:
                    if level_nodes: 
                        print(f"Level {current_level}: {level_nodes}")
                    level_nodes = [] 
                    current_level = level
                level_nodes.append(node.keys)
                if not node.is_leaf:
                    for child in node.children:
                        queue.append((child, level + 1))
            if level_nodes:
                print(f"Level {current_level}: {level_nodes}")

                

    def min_keys(self):
        return (self.max_degree + 1) // 2 - 1


    def delete(self, key):
        leaf = self.find_leaf(self.root, key)
        if key not in leaf.keys:
            print(f"Key {key} not found in the tree.")
            return
        leaf.keys.remove(key)
        if len(leaf.keys) >= self.min_keys():
            self.update_internal_nodes(self.root, key)
            return

        parent = self.find_parent(self.root, leaf)
        left_sibling, right_sibling = self.get_siblings(parent, leaf)

        if left_sibling and len(left_sibling.keys) > self.min_keys():
            self.borrow_from_left(leaf, left_sibling, parent)
        elif right_sibling and len(right_sibling.keys) > self.min_keys():
            self.borrow_from_right(leaf, right_sibling, parent)
        else:
            if left_sibling:
                self.merge_nodes(left_sibling, leaf, parent)
            elif right_sibling:
                self.merge_nodes(leaf, right_sibling, parent)

        self.update_internal_nodes(self.root, key)

        if key in self.root.keys:
            index = self.root.keys.index(key)
            if not self.root.is_leaf:
                self.root.keys[index] = self.find_smallest(self.root.children[index + 1])

        if self.root.keys == [] and not self.root.is_leaf:
            self.root = self.root.children[0]



    def update_internal_nodes(self, node, key):
        if node.is_leaf:
            return

        for i, item in enumerate(node.keys):
            if item == key:
                node.keys[i] = self.find_smallest(node.children[i + 1])
                break

        for child in node.children:
            self.update_internal_nodes(child, key)


    def find_smallest(self, node):
        while not node.is_leaf:
            node = node.children[0]
        return node.keys[0]


    def get_siblings(self, parent, node):
        index = parent.children.index(node)
        left_sibling = parent.children[index - 1] if index > 0 else None
        right_sibling = parent.children[index + 1] if index < len(parent.children) - 1 else None
        return left_sibling, right_sibling


    def borrow_from_right(self, node, right_sibling, parent):
        borrow_key = right_sibling.keys.pop(0)
        node.keys.append(parent.keys[parent.children.index(node)])
        parent.keys[parent.children.index(node)] = right_sibling.keys[0]

        if not node.is_leaf:
            node.children.append(right_sibling.children.pop(0))

    def borrow_from_right_internal(self, node, right_sibling, parent):
        borrow_key = right_sibling.keys.pop(0) 
        node.keys.append(parent.keys[parent.children.index(node)]) 
        parent.keys[parent.children.index(node)] = borrow_key

        if not node.is_leaf:
            node.children.append(right_sibling.children.pop(0))

    def borrow_from_left(self, node, left_sibling, parent):
        borrow_key = left_sibling.keys.pop(-1)
        parent.keys[parent.children.index(node) - 1] = borrow_key
        node.keys.insert(0, parent.keys[parent.children.index(node) - 1])

        if not node.is_leaf:
            node.children.insert(0, left_sibling.children.pop(-1))
 
    def borrow_from_left_internal(self, node, left_sibling, parent):
        borrow_key = left_sibling.keys.pop(-1)
        node.keys.insert(0, parent.keys[parent.children.index(node) - 1])
        parent.keys[parent.children.index(node) - 1] = borrow_key

        if not node.is_leaf:
            node.children.insert(0, left_sibling.children.pop(-1))

   
    def merge_nodes(self, left_node, right_node, parent):
       
        merge_key = parent.keys[parent.children.index(left_node)]
        # left_node.keys.append(merge_key)
        left_node.keys.extend(right_node.keys)

        if not left_node.is_leaf:
            left_node.children.extend(right_node.children) 

        parent.keys.remove(merge_key)
        parent.children.remove(right_node)

        if not parent.keys:
            self.merge_internal_nodes(parent)

    
    def merge_internal_nodes(self, node):
        if node == self.root:
            if len(node.keys) == 0:
                self.root = node.children[0]
                # print("Tree height decreased. New root:", self.root.keys)
            return

        parent = self.find_parent(self.root, node)

        index = parent.children.index(node)
        left_sibling = None
        right_sibling = None

        if index > 0:
            left_sibling = parent.children[index - 1]
        if index < len(parent.children) - 1:
            right_sibling = parent.children[index + 1]

        if left_sibling and len(left_sibling.keys) > self.min_keys():
            self.borrow_from_left_internal(node, left_sibling, parent)
            # print(f"Borrowed from left sibling: {left_sibling.keys}")
            return

        if right_sibling and len(right_sibling.keys) > self.min_keys():
            self.borrow_from_right_internal(node, right_sibling, parent)
            # print(f"Borrowed from right sibling: {right_sibling.keys}")
            return

        if left_sibling:
            merge_key = parent.keys.pop(index - 1)
            left_sibling.keys.append(merge_key)
            left_sibling.keys.extend(node.keys)
            left_sibling.children.extend(node.children)
            parent.children.remove(node)
            # print(f"Merged with left sibling: {left_sibling.keys}")
        elif right_sibling:
            merge_key = parent.keys.pop(index)
            node.keys.append(merge_key)
            node.keys.extend(right_sibling.keys)
            node.children.extend(right_sibling.children)
            parent.children.remove(right_sibling)
            # print(f"Merged with right sibling: {node.keys}")

        if not parent.keys:
            self.merge_internal_nodes(parent)


    def clear(self):
        self.root = None 
        self.root = Node(is_leaf=True)



if __name__ == "__main__":

    from GUI import start_visualizer 
    tree = BPlusTree(max_degree=3)
    start_visualizer(tree)
    # tree = BPlusTree(max_degree=3)
    # # for key in [1,4,7,10]:
    # #     # 17,21,31,25,19,20,28,42
    # #     tree.insert(key)
 