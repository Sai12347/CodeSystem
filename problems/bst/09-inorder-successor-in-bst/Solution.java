class Solution {
    public TreeNode inorderSuccessor(TreeNode root, TreeNode p) {
        TreeNode succ = null;
        TreeNode curr = root;
        while (curr != null) {
            if (p.val < curr.val) {
                succ = curr;
                curr = curr.left;
            } else {
                curr = curr.right;
            }
        }
        return succ;
    }
}
