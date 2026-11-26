class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        vals = []

        def inorder(node: Optional[TreeNode]) -> None:
            if not node:
                return
            inorder(node.left)
            vals.append(node.val)
            inorder(node.right)

        inorder(root)
        return all(vals[i] < vals[i + 1] for i in range(len(vals) - 1))
