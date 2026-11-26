class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        in_index = {val: idx for idx, val in enumerate(inorder)}
        pre_idx = 0

        def helper(left: int, right: int) -> Optional[TreeNode]:
            nonlocal pre_idx
            if left > right:
                return None
            root_val = preorder[pre_idx]
            pre_idx += 1
            root = TreeNode(root_val)
            mid = in_index[root_val]
            root.left = helper(left, mid - 1)
            root.right = helper(mid + 1, right)
            return root

        return helper(0, len(inorder) - 1)
