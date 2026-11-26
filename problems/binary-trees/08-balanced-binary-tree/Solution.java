class Solution {
    public boolean isBalanced(TreeNode root) {
        return check(root) != -1;
    }

    private int check(TreeNode node) {
        if (node == null) return 0;
        int lh = check(node.left);
        if (lh == -1) return -1;
        int rh = check(node.right);
        if (rh == -1 || Math.abs(lh - rh) > 1) return -1;
        return 1 + Math.max(lh, rh);
    }
}
