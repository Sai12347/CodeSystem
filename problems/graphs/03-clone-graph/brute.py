class Solution:
    def cloneGraph(self, node: "Optional[Node]") -> "Optional[Node]":
        if node is None:
            return None
        clones = {node: Node(node.val)}
        q = deque([node])
        while q:
            cur = q.popleft()
            for nb in cur.neighbors:
                if nb not in clones:
                    clones[nb] = Node(nb.val)
                    q.append(nb)
                clones[cur].neighbors.append(clones[nb])
        return clones[node]
