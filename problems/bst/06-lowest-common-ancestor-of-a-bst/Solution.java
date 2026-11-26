class Solution {
    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        TreeNode cur = root;
        int pv = p.val;
        int qv = q.val;
        while (cur != null) {
            if (pv < cur.val && qv < cur.val) {
                cur = cur.left;
            } else if (pv > cur.val && qv > cur.val) {
                cur = cur.right;
            } else {
                return cur;
            }
        }
        return null;
    }
}
