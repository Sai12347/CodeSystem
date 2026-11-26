class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        if not preorder:
            return None
        root_val = preorder[0]
        mid = inorder.index(root_val)
        root = TreeNode(root_val)
        root.left = self.buildTree(preorder[1 : 1 + mid], inorder[:mid])
        root.right = self.buildTree(preorder[1 + mid :], inorder[mid + 1 :])
        return root
