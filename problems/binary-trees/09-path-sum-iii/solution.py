class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:
        prefix = defaultdict(int)
        prefix[0] = 1

        def dfs(node: Optional[TreeNode], cur: int) -> int:
            if not node:
                return 0
            cur += node.val
            count = prefix[cur - targetSum]
            prefix[cur] += 1
            count += dfs(node.left, cur)
            count += dfs(node.right, cur)
            prefix[cur] -= 1
            return count

        return dfs(root, 0)
