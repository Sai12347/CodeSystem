class Solution {
    private int best;

    public int diameterOfBinaryTree(TreeNode root) {
        best = 0;
        height(root);
        return best;
    }

    private int height(TreeNode node) {
        if (node == null) return 0;
        int lh = height(node.left);
        int rh = height(node.right);
        if (lh + rh > best) best = lh + rh;
        return 1 + Math.max(lh, rh);
    }
}
