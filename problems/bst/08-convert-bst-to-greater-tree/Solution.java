class Solution {
    public TreeNode convertBST(TreeNode root) {
        int runningSum = 0;
        TreeNode curr = root;
        while (curr != null) {
            if (curr.right == null) {
                runningSum += curr.val;
                curr.val = runningSum;
                curr = curr.left;
            } else {
                TreeNode succ = curr.right;
                while (succ.left != null && succ.left != curr) {
                    succ = succ.left;
                }
                if (succ.left == null) {
                    succ.left = curr;
                    curr = curr.right;
                } else {
                    succ.left = null;
                    runningSum += curr.val;
                    curr.val = runningSum;
                    curr = curr.left;
                }
            }
        }
        return root;
    }
}
