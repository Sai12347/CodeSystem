class Solution:
    def lowestCommonAncestor(
        self,
        root: "Optional[TreeNode]",
        p: "TreeNode",
        q: "TreeNode",
    ) -> "Optional[TreeNode]":
        def find_path(node, target, path):
            if node is None:
                return False
            path.append(node)
            if node is target:
                return True
            if find_path(node.left, target, path) or find_path(node.right, target, path):
                return True
            path.pop()
            return False

        path_p = []
        path_q = []
        find_path(root, p, path_p)
        find_path(root, q, path_q)

        lca = None
        for a, b in zip(path_p, path_q):
            if a is b:
                lca = a
            else:
                break
        return lca
