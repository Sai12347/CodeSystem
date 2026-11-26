class PersistentMinStack:
    def __init__(self):
        self.val = [0]
        self.min_val = [0]
        self.parent = [0]
        self.ver_node = [0]  # version 0 -> empty sentinel node 0

    def push(self, version: int, val: int) -> int:
        p = self.ver_node[version]
        mn = val if p == 0 or val < self.min_val[p] else self.min_val[p]
        node_id = len(self.val)
        self.val.append(val)
        self.min_val.append(mn)
        self.parent.append(p)
        self.ver_node.append(node_id)
        return len(self.ver_node) - 1

    def pop(self, version: int) -> int:
        p = self.ver_node[version]
        self.ver_node.append(self.parent[p])
        return len(self.ver_node) - 1

    def top(self, version: int) -> int:
        return self.val[self.ver_node[version]]

    def getMin(self, version: int) -> int:
        return self.min_val[self.ver_node[version]]
