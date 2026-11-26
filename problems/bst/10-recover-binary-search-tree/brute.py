class Solution:
    def recoverTree(self, root: Optional[TreeNode]) -> None:
        nodes = []

        def inorder(node: Optional[TreeNode]) -> None:
            if node is None:
                return
            inorder(node.left)
            nodes.append(node)
            inorder(node.right)

        inorder(root)
        vals = sorted(node.val for node in nodes)
        for node, v in zip(nodes, vals):
            node.val = v
