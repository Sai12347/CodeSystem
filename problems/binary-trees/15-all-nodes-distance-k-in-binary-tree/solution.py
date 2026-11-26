class Solution:
    def distanceK(
        self,
        root: "Optional[TreeNode]",
        target: "TreeNode",
        k: int,
    ) -> List[int]:
        if root is None or target is None:
            return []
        parent = {}
        q = deque([root])
        while q:
            node = q.popleft()
            if node.left is not None:
                parent[node.left] = node
                q.append(node.left)
            if node.right is not None:
                parent[node.right] = node
                q.append(node.right)

        bfs = deque([target])
        visited = {target}
        dist = 0
        while bfs and dist < k:
            for _ in range(len(bfs)):
                curr = bfs.popleft()
                for nxt in (curr.left, curr.right, parent.get(curr)):
                    if nxt is not None and nxt not in visited:
                        visited.add(nxt)
                        bfs.append(nxt)
            dist += 1

        return [node.val for node in bfs]
