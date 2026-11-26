class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:
        def count_from(node: Optional[TreeNode], rem: int) -> int:
            if not node:
                return 0
            rem -= node.val
            return (1 if rem == 0 else 0) + count_from(node.left, rem) + count_from(node.right, rem)

        def dfs(node: Optional[TreeNode]) -> int:
            if not node:
                return 0
            return count_from(node, targetSum) + dfs(node.left) + dfs(node.right)

        return dfs(root)
