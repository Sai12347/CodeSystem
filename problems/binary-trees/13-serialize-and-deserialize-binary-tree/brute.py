class Codec:
    def serialize(self, root: "Optional[TreeNode]") -> str:
        out = []

        def dfs(node):
            if node is None:
                out.append("N")
                return
            out.append(str(node.val))
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return " ".join(out)

    def deserialize(self, data: str) -> "Optional[TreeNode]":
        tokens = iter(data.split())

        def dfs():
            tok = next(tokens)
            if tok == "N":
                return None
            node = TreeNode(int(tok))
            node.left = dfs()
            node.right = dfs()
            return node

        return dfs()
