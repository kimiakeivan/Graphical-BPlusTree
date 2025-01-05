from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsTextItem
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtCore import Qt
import sys


class Node:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf     
        self.keys = []             
        self.children = []          
        self.next = None 
        self.parent = None          



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
            # print(new_node.keys)
            new_node.children =node.children[mid_index+1:]
            node.children = node.children[:mid_index+1]
            # for i in new_node.children:
            #     print(i.keys)

        

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
                # print("before ",parent.keys)
                self.split(parent)
                # print("after ",parent.keys)




    
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
            for i,key in enumerate(node.keys):
                if searchkey < key:
                        node = node.children[i]
                        break
            else:
                    node = node.children[-1]     


        for i, key in enumerate(node.keys):
            if key == searchkey:
                return True
        return False    




    def delete(self):
        pass

    def merge(self):
        pass




    
    
tree = BPlusTree(max_degree=4)
tree.insert(10)
tree.insert(20)
tree.insert(5)
tree.insert(15)
tree.insert(25)
tree.insert(11)
tree.insert(13)
tree.insert(40)
tree.insert(4)
tree.insert(22)
tree.insert(36)
tree.insert(17)
print(tree.search(11))


print("Root keys:", tree.root.keys)
# print("Child 1 keys:", tree.root.children[0].children[0].keys)
# print("Child 2 keys:", tree.root.children[1].keys)
# print("Child 2 keys:", tree.root.children[1].keys)

for i, child in enumerate(tree.root.children):
    print(f"child{i} keys: {child.keys}")
    for j, childen in enumerate(child.children):
        print(f"child{j} keys: {childen.keys}")






# class TreeVisualizer(QGraphicsView):
#     def __init__(self, tree):
#         super().__init__()
#         self.tree = tree
#         self.scene = QGraphicsScene()
#         self.setScene(self.scene)
#         self.draw_tree()

#     def draw_tree(self):
#         self.scene.clear()
#         self._draw_node(self.tree.root, 0, 400, 200)

#     def _draw_node(self, node, depth, x, y):
#         # Draw node
#         node_item = QGraphicsEllipseItem(x - 30, y - 20, 70, 40)
#         node_item.setBrush(QBrush(Qt.white))
#         node_item.setPen(QPen(Qt.black))
#         self.scene.addItem(node_item)

#         # Draw keys inside node
#         keys_text = QGraphicsTextItem(", ".join(map(str, node.keys)))
#         keys_text.setPos(x - 25, y - 15)
#         self.scene.addItem(keys_text)

#         # Recursively draw children
#         if not node.is_leaf:
#             step = 50 * len(node.children)
#             for i, child in enumerate(node.children):
#                 child_x = x - step // 2 + i * 100
#                 child_y = y + 150

#                 # Draw line from parent to child
#                 self.scene.addLine(x, y + 20, child_x, child_y - 20, QPen(Qt.black))

#                 self._draw_node(child, depth + 1, child_x, child_y)

# # Main code
# if __name__ == "__main__":
#     app = QApplication(sys.argv)

#     # Build B+ tree
#     tree = BPlusTree(max_degree=4)
#     for key in [10, 20, 5, 15, 25, 11, 13, 40, 4, 22, 36, 17]:
#         tree.insert(key)

#     # Visualize the tree
#     visualizer = TreeVisualizer(tree)
#     visualizer.setWindowTitle("B+ Tree Visualization")
#     visualizer.show()

#     sys.exit(app.exec_())
