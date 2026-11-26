class Adapter {
    @SuppressWarnings("unchecked")
    public static Object run(Map<String, Object> inp) {
        List<Object> raw = (List<Object>) inp.get("nums");
        int n = raw.size();
        int[] orig = new int[n];
        int[] copy = new int[n];
        for (int i = 0; i < n; i++) {
            orig[i] = ((Number) raw.get(i)).intValue();
            copy[i] = orig[i];
        }
        TreeNode root = new Solution().sortedArrayToBST(copy);
        if (root == null) {
            return "Expected a non-empty TreeNode, got null";
        }
        Set<TreeNode> visited = Collections.newSetFromMap(new IdentityHashMap<>());
        List<Integer> inorder = new ArrayList<>(n);
        String[] err = new String[1];
        dfs(root, n, visited, inorder, err);
        if (err[0] != null) {
            return err[0];
        }
        if (inorder.size() != n) {
            return "Expected " + n + " nodes, got " + inorder.size();
        }
        for (int i = 0; i < n; i++) {
            if (inorder.get(i) != orig[i]) {
                return "Inorder traversal does not match sorted input array (not a valid BST of nums)";
            }
        }
        return true;
    }

    private static int dfs(TreeNode node, int n, Set<TreeNode> visited, List<Integer> inorder, String[] err) {
        if (node == null || err[0] != null) {
            return 0;
        }
        if (!visited.add(node)) {
            err[0] = "Returned tree contains a cycle or shared node reference";
            return 0;
        }
        if (visited.size() > n) {
            err[0] = "Returned tree has more than " + n + " nodes";
            return 0;
        }
        int lh = dfs(node.left, n, visited, inorder, err);
        if (err[0] != null) {
            return 0;
        }
        inorder.add(node.val);
        int rh = dfs(node.right, n, visited, inorder, err);
        if (err[0] != null) {
            return 0;
        }
        if (Math.abs(lh - rh) > 1) {
            err[0] = "Tree is not height-balanced at node " + node.val + " (left height " + lh + ", right height " + rh + ")";
            return 0;
        }
        return 1 + Math.max(lh, rh);
    }
}
