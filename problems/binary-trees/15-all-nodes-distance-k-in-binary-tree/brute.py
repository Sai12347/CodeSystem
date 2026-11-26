class Solution:
    def distanceK(
        self,
        root: "Optional[TreeNode]",
        target: "TreeNode",
        k: int,
    ) -> List[int]:
        adj = defaultdict(list)

        def build(node):
            if node is None:
                return
            if node.left is not None:
                adj[node.val].append(node.left.val)
                adj[node.left.val].append(node.val)
                build(node.left)
            if node.right is not None:
                adj[node.val].append(node.right.val)
                adj[node.right.val].append(node.val)
                build(node.right)

        build(root)
        ans = []

        def dfs(u, prev, d):
            if d == k:
                ans.append(u)
                return
            for v in adj[u]:
                if v != prev:
                    dfs(v, u, d + 1)

        dfs(target.val, None, 0)
        return ans
