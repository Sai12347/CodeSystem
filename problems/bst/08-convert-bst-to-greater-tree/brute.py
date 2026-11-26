class Solution:
    def convertBST(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if root is None:
            return None
        nodes = []
        stack = [root]
        while stack:
            node = stack.pop()
            nodes.append(node)
            if node.left is not None:
                stack.append(node.left)
            if node.right is not None:
                stack.append(node.right)
        orig_vals = [node.val for node in nodes]
        for node in nodes:
            v = node.val
            node.val = sum(x for x in orig_vals if x >= v)
        return root
