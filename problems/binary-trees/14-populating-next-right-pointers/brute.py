class Solution:
    def connect(self, root: "Optional[Node]") -> "Optional[Node]":
        if root is None:
            return None
        q = deque([root])
        while q:
            size = len(q)
            for i in range(size):
                node = q.popleft()
                node.next = q[0] if i + 1 < size else None
                if node.left is not None:
                    q.append(node.left)
                if node.right is not None:
                    q.append(node.right)
        return root
