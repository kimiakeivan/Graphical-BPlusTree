import math


class Node:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf      # is this node a leaf?
        self.keys = []              # for keys
        self.children = []          #for internal nodes
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
    def insert(self, key, pointer):
        if key == None or pointer == None:
            print('Inserting None?')
            return
        leaf = None
        if self.root == None:
            self.root = Node(is_leaf=True)
            leaf = self.root
        else:
            leaf = self.find_leaf(key)

        if len(leaf.keys) < self.max_degree-1:
            self.insert_leaf(leaf, key, pointer)
        else:
            leaf_t = Node(is_leaf=True)
            temp = self.copy_tempo(leaf)
            self.insert_leaf(temp, key, pointer)

            if(leaf.children[-1] is Node): 
                leaf_t.children.append(leaf.children[-1])
            leaf.children = [leaf_t]
            leaf.keys.clear()

            border = int(math.ceil(self.max_degree/2))

            leaf.keys = temp.keys[:border]
            leaf.children = temp.children[:border] + leaf.children

            leaf_t.keys = temp.keys[border:]
            leaf_t.children += temp.children[border:]   # changed this from book

            k_t = leaf_t.keys[0] 
            self.insert_parent(leaf, k_t, leaf_t)


    def copy_tempo(self, node, full=False):
        temp = Node(is_leaf= node.is_leaf)
        c = 0 if full else 1
        if self.right(node):
            c = 0
        temp.keys = node.keys[:]
        temp.children = node.children[:len(node.children)-c]
        return temp


    def insert_leaf(self, leaf, key, pointer):
        if leaf == self.root and len(leaf.keys) == 0:
            leaf.keys = [key]
            leaf.children = [pointer]
            return

        if key < leaf.keys[0]:
            leaf.keys.insert(0, key)
            leaf.children.insert(0, pointer)
        else:
            self.add_key_child(leaf, key, pointer)



    def insert_parent(self, node, k_t, node_t):
        if node == self.root:
            node_r = Node()
            node_r.keys = [k_t]
            node_r.children = [node, node_t]
            self.root = node_r
            return

        node_p = self.parent(node)
        if len(node_p.children) < self.max_degree:
            index = node_p.children.index(node)
            node_p.children.insert(index+1, node_t)
            node_p.keys.insert(index, k_t)
        else:

            temp = self.copy_tempo(node_p, full=True)
            index = temp.children.index(node)
            temp.children.insert(index+1, node_t) # test if +1 is needed
            temp.keys.insert(index, k_t)

            node_p.keys.clear()
            node_p.children.clear()
            node_p_t = Node()
            border = int(math.ceil((self.max_degree+1)/2))
            node_p.keys = temp.keys[:border-1]
            node_p.children = temp.children[:border]
            k_tt = temp.keys[border-1]
            node_p_t.keys = temp.keys[border:]
            node_p_t.children = temp.children[border:]

            self.insert_parent(node_p, k_tt, node_p_t)



    def find_leaf(self, key):
        curr_node = self.root
        while not curr_node.is_leaf:
            i = 0
            while i < len(curr_node.keys) and key >= curr_node.keys[i]:
                i += 1
            curr_node = curr_node.children[i]
        return curr_node


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


    def parent(self, node):
        if self.root == node:
            return None
        return self.find_parent(self.root, node)


    def find_parent(self, curr_node, child_node):
        if curr_node.is_leaf:
            return None
        for child in curr_node.children:
            if child == child_node:
                return curr_node
            parent = self.find_parent(child, child_node)
            if parent:
                return parent
        return None

    # TODO: add function to merge nodes after deletion
    def delete(self, key, child):
        leaf = self.find_leaf(key)
        self.delete_query(leaf, key, child)


    def delete_query(self, node, key, child):
        node.keys.remove(key)
        node.children.remove(child)

        if self.root == node and self.root.is_leaf:
            if len(self.root.keys) == 0:
                del node
                self.root = None
            return
        else_if_condition = len(node.children) < int(math.ceil(self.max_degree/2))
        if node.is_leaf:
            print("debug3")
            else_if_condition = len(node.keys) < int(math.ceil((self.max_degree-1)/2))

        if node == self.root and len(node.children) == 1:
            print("debug2")
            self.root = node.children[0]
            del node

        elif else_if_condition:
            print("debug")
            node_tempo = self.get_sibs(node)
            parent = self.parent(node)
            index = parent.children.index(node_tempo)
            index_2 = parent.children.index(node)
            key_tempo = parent.keys[index] if index < index_2 else parent.keys[index_2]

            if len(node.keys) + len(node_tempo.keys) <= self.max_degree-1:
                if self.is_predum(node, node_tempo):
                    node, node_tempo = node_tempo, node

                self.merge(node_tempo, node, key_tempo)
                self.delete_query(self.parent(node), key_tempo, node)
                del node

            else:
                if self.is_predum(node_tempo, node):
                    if not(node.is_leaf) and not(node == self.root):
                        main_key = node_tempo.keys.pop()
                        main = node_tempo.children.pop()
                        node.keys.insert(0, key_temp)
                        node.children.insert(0, main)
                        parent.keys[parent.keys.index(key_tempo)] = main_key

                    else:
                        main_key = node_t.keys.pop()
                        main_child = node_tempo.children.pop()
                        node.keys.insert(0, main_key)
                        node.children.insert(0, main_child)
                        parent.keys[parent.keys.index(key_tempo)] = main_key

                else:
                    if not(node.is_leaf) and not(node == self.root):
                        node_tempo.keys.pop(0)
                        main = node_tempo.children.pop(0)
                        node.keys.append(key_tempo)
                        node.children.append(main)
                        parent.keys[parent.keys.index(key_tempo)] = node_tempo.keys[0]

                    else:
                        main_key = node_tempo.keys.pop(0)
                        main_child = node_tempo.children.pop(0)
                        node.keys.append(main_key)
                        node.children.append(main_child)
                        parent.keys[parent.keys.index(key_tempo)] = node_tempo.keys[0]


    def is_predum(self, node, node_tempo):
        current = self.root
        while current is not node_tempo:
            temp = self.find_key(current, node_tempo.keys[0])
            if temp > 0 and current.children[temp - 1] is node:
                return True
            current = current.children[temp]
        return False


    def find_key(self, current, node_tempo_keys):
        temp = 0
        while temp < len(current.keys) and current.keys[temp] <= node_tempo_keys:
            temp += 1
        return temp


    def get_sibs(self, node):
        parent = self.parent(node)
        index = parent.children.index(node)

        if index > 0:
            return parent.children[index - 1]
        else:
            return parent.children[index + 1]


    def merge(self, node_tempo, node, key_tempo):
        if not(node.is_leaf):
            self.add_key(node_tempo, key_tempo)

            for k in range(0, len(node.keys)):
                self.add_key_child(node_tempo, node.keys[k], node.children[i])
            self.add_merge_child(node_tempo, node.children[-1])

        else:
            if len(node.keys) > 0:
                self.merge_leaf(node_tempo, node)
                node_tempo.children[-1] = node.children[-1]

            if self.right(node):
                node_tempo.children.pop()


    def right(self, node):
        current = self.root
        while not(current.is_leaf):
            current = current.children[-1]
        return current == node


    def merge_leaf(self, node_tempo, node):
        index = 0
        while index < len(node_tempo.keys):
            if node_tempo.keys[index] > node.keys[0]:
                break
            index += 1

        for k in range(0, len(node.keys)):
            node_tempo.keys.insert(index+k, node.keys[k])
            node_tempo.children.insert(index+k, node.children[k])


    def add_key(self, node, key):
        i = 0
        while i < len(node.keys):
            node.keys.insert(i, key)
            return
        i += 1
        node.keys.append(key)


    def add_key_child(self, node, key, child):
        i = 0
        while i < len(node.keys):
            if node.keys[i] > key:
                node.keys.insert(i, key)
                node.children.insert(i, child)
                return i
            i += 1
        node.keys.append(key)
        node.children.append(child)
        return i


    def add_merge_child(self, node_tempo, child):
        element = child.keys[-1]
        position = 0
        for node in node_tempo.children:
            c = node.keys[0]
            if element < c:
                break
            position += 1
        node_tempo.children.insert(position, child)


    def search(self):
        pass


    def get_dict(self):
        if self.root == None:
            return {'root': {}}
        return {'root': self.root.get_dict()}


# Add this if __name__ == "__main__" in case you wanted to import this file for graphical view
if __name__ == "__main__":
    bpt = BPlusTree(3)
    bpt.insert(1, 1)
    bpt.insert(2, 2)
    bpt.insert(3, 3)
    bpt.insert(4, 4)
    bpt.insert(5, 5)
    bpt.insert(6, 6)
    bpt.insert(7, 7)
    bpt.insert(9, 9)
    print(bpt.get_dict())
    bpt.delete(1, 1)
    print(bpt.get_dict())
