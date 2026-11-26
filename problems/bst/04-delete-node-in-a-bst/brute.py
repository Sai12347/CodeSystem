class Solution:
    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        vals = []

        def inorder(node: Optional[TreeNode]) -> None:
            if not node:
                return
            inorder(node.left)
            if node.val != key:
                vals.append(node.val)
            inorder(node.right)

        inorder(root)

        def build(lo: int, hi: int) -> Optional[TreeNode]:
            if lo > hi:
                return None
            mid = (lo + hi) // 2
            return TreeNode(vals[mid], build(lo, mid - 1), build(mid + 1, hi))

        return build(0, len(vals) - 1)
