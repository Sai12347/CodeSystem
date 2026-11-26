class Solution:
    def buildTree(self, inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
        in_index = {val: idx for idx, val in enumerate(inorder)}
        post_idx = len(postorder) - 1

        def helper(left: int, right: int) -> Optional[TreeNode]:
            nonlocal post_idx
            if left > right:
                return None
            root_val = postorder[post_idx]
            post_idx -= 1
            root = TreeNode(root_val)
            mid = in_index[root_val]
            root.right = helper(mid + 1, right)
            root.left = helper(left, mid - 1)
            return root

        return helper(0, len(inorder) - 1)
