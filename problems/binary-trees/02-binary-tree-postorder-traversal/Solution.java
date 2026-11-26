class Solution {
    public List<Integer> postorderTraversal(TreeNode root) {
        List<Integer> res = new ArrayList<>();
        Deque<TreeNode> stack = new ArrayDeque<>();
        TreeNode cur = root;
        TreeNode lastVisited = null;
        while (cur != null || !stack.isEmpty()) {
            while (cur != null) {
                stack.push(cur);
                cur = cur.left;
            }
            TreeNode peek = stack.peek();
            if (peek.right != null && lastVisited != peek.right) {
                cur = peek.right;
            } else {
                res.add(peek.val);
                lastVisited = stack.pop();
            }
        }
        return res;
    }
}
