class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        levels: List[List[int]] = []

        def dfs(node: Optional[TreeNode], depth: int) -> None:
            if not node:
                return
            if depth == len(levels):
                levels.append([])
            levels[depth].append(node.val)
            dfs(node.left, depth + 1)
            dfs(node.right, depth + 1)

        dfs(root, 0)
        return levels
