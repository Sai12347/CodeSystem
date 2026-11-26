class Solution:
    def cloneGraph(self, node: "Optional[Node]") -> "Optional[Node]":
        if node is None:
            return None

        clones = {}

        def dfs(cur: "Node") -> "Node":
            if cur in clones:
                return clones[cur]
            copy = Node(cur.val)
            clones[cur] = copy
            for nb in cur.neighbors:
                copy.neighbors.append(dfs(nb))
            return copy

        return dfs(node)
