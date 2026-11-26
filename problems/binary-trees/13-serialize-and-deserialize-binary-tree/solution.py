class Codec:
    def serialize(self, root: "Optional[TreeNode]") -> str:
        if root is None:
            return ""
        out = []
        q = deque([root])
        while q:
            node = q.popleft()
            if node is None:
                out.append("#")
            else:
                out.append(str(node.val))
                q.append(node.left)
                q.append(node.right)
        return ",".join(out)

    def deserialize(self, data: str) -> "Optional[TreeNode]":
        if not data:
            return None
        tokens = data.split(",")
        root = TreeNode(int(tokens[0]))
        q = deque([root])
        i = 1
        while q and i < len(tokens):
            node = q.popleft()
            if tokens[i] != "#":
                node.left = TreeNode(int(tokens[i]))
                q.append(node.left)
            i += 1
            if i < len(tokens) and tokens[i] != "#":
                node.right = TreeNode(int(tokens[i]))
                q.append(node.right)
            i += 1
        return root
