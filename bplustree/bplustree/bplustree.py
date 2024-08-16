class BPlusTreeNode:
    def __init__(self, is_leaf=False):
        """Initializes a B+ tree node."""
        self.keys = []
        self.children = []
        self.is_leaf = is_leaf

    def __str__(self):
        """String representation of a B+ tree node."""
        return str(self.keys)


class BPlusTree:
    def __init__(self, fanout):
        """
        Initializes a B+ tree.

        Args:
            fanout (int): The maximum number of children per node. Default is 4.
        """
        self.root = BPlusTreeNode(is_leaf=True)
        self.fanout = fanout
        self.leaf_counter = 0

    def insert(self, key):
        """
        Inserts a key into the B+ tree.

        Args:
            key: The key to be inserted.
        """
        root = self.root
        if len(root.keys) == self.fanout - 1:
            new_root = BPlusTreeNode()
            new_root.children.append(root)
            self._split_child(new_root, 0)
            self.root = new_root
        self._insert_non_full(self.root, key)

    def delete(self, key):
        """
        Deletes a key from the B+ tree.

        Args:
            key: The key to be deleted.
        """
        if not self.root:
            raise ValueError("Tree is empty.")

        self._delete(self.root, key)

        if len(self.root.keys) == 0 and not self.root.is_leaf:
            self.root = self.root.children[0]
    
    def _insert_non_full(self, node, key):
        if node.is_leaf:
            node.keys.append(key)
            node.keys.sort()
        else:
            i = len(node.keys) - 1
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            child = node.children[i]
            if len(child.keys) == self.fanout - 1:
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key)

    def _split_child(self, parent, index):
        node_to_split = parent.children[index]
        mid_index = len(node_to_split.keys) // 2

        new_node = BPlusTreeNode(is_leaf=node_to_split.is_leaf)
        parent.keys.insert(index, node_to_split.keys[mid_index])
        parent.children.insert(index + 1, new_node)

        new_node.keys = node_to_split.keys[mid_index + 1:]
        node_to_split.keys = node_to_split.keys[:mid_index]

        if not node_to_split.is_leaf:
            new_node.children = node_to_split.children[mid_index + 1:]
            node_to_split.children = node_to_split.children[:mid_index + 1]

    def _delete(self, node, key):
        if node.is_leaf:
            if key in node.keys:
                node.keys.remove(key)
        else:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1

            if i < len(node.keys) and key == node.keys[i]:
                if len(node.children[i].keys) >= (self.fanout + 1) // 2:
                    predecessor = self._get_predecessor(node, i)
                    node.keys[i] = predecessor
                    self._delete(node.children[i], predecessor)
                elif len(node.children[i + 1].keys) >= (self.fanout + 1) // 2:
                    successor = self._get_successor(node, i)
                    node.keys[i] = successor
                    self._delete(node.children[i + 1], successor)
                else:
                    self._merge(node, i)
                    self._delete(node.children[i], key)
            else:
                if len(node.children[i].keys) == (self.fanout + 1) // 2 - 1:
                    if i > 0 and len(node.children[i - 1].keys) >= (self.fanout + 1) // 2:
                        self._borrow_from_prev(node, i)
                    elif i < len(node.children) - 1 and len(node.children[i + 1].keys) >= (self.fanout + 1) // 2:
                        self._borrow_from_next(node, i)
                    else:
                        if i < len(node.children) - 1:
                            self._merge(node, i)
                        else:
                            self._merge(node, i - 1)
                            i -= 1
                self._delete(node.children[i], key)

    def _merge(self, parent, index):
        child = parent.children[index]
        sibling = parent.children[index + 1]

        if not child.is_leaf:
            child.keys.append(parent.keys[index])
            child.keys.extend(sibling.keys)
            child.children.extend(sibling.children)
        else:
            child.keys.extend(sibling.keys)

        parent.keys.pop(index)
        parent.children.pop(index + 1)

    def _borrow_from_prev(self, parent, index):
        child = parent.children[index]
        sibling = parent.children[index - 1]

        if not child.is_leaf:
            child.children.insert(0, sibling.children.pop())
            child.keys.insert(0, parent.keys[index - 1])
            parent.keys[index - 1] = sibling.keys.pop()
        else:
            child.keys.insert(0, sibling.keys.pop())
            parent.keys[index - 1] = sibling.keys[-1]

    def _borrow_from_next(self, parent, index):
        child = parent.children[index]
        sibling = parent.children[index + 1]

        if not child.is_leaf:
            child.children.append(sibling.children.pop(0))
            child.keys.append(parent.keys[index])
            parent.keys[index] = sibling.keys.pop(0)
        else:
            child.keys.append(sibling.keys.pop(0))
            parent.keys[index] = sibling.keys[0]

    def _get_predecessor(self, node, index):
        current = node.children[index]
        while not current.is_leaf:
            current = current.children[-1]
        return current.keys[-1]

    def _get_successor(self, node, index):
        current = node.children[index + 1]
        while not current.is_leaf:
            current = current.children[0]
        return current.keys[0]
    
    def print_tree(self, node=None, level=0):
        if node is None:
            node = self.root
        
        lines = []
        indent = " " * (level * 4)
        lines.append(f"{indent}Level {level}: {node.keys}")
        
        if not node.is_leaf:
            for child in node.children:
                lines.extend(self.print_tree(child, level + 1))
        else:
            lines.append(f"{indent}Leaf Node: {node.keys}")

        return lines

    def print_tree_state(self):
        return "\n".join(self.print_tree())
