class Solution:
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        cur = root
        pv, qv = p.val, q.val
        while cur is not None:
            if pv < cur.val and qv < cur.val:
                cur = cur.left
            elif pv > cur.val and qv > cur.val:
                cur = cur.right
            else:
                return cur
        return cur
