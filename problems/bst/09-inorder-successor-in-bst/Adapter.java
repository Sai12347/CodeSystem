class Adapter {
    @SuppressWarnings("unchecked")
    public static Object run(Map<String, Object> inp) {
        TreeNode root = Judge.buildTree((List<Object>) inp.get("root"));
        int targetVal = ((Number) inp.get("p")).intValue();
        IdentityHashMap<TreeNode, Integer> origVals = new IdentityHashMap<>();
        TreeNode pNode = null;

        ArrayDeque<TreeNode> stack = new ArrayDeque<>();
        if (root != null) {
            stack.push(root);
        }
        while (!stack.isEmpty()) {
            TreeNode node = stack.pop();
            origVals.put(node, node.val);
            if (node.val == targetVal) {
                pNode = node;
            }
            if (node.right != null) {
                stack.push(node.right);
            }
            if (node.left != null) {
                stack.push(node.left);
            }
        }
        if (pNode == null) {
            throw new IllegalStateException("Target node p=" + targetVal + " not found in tree");
        }

        TreeNode res = new Solution().inorderSuccessor(root, pNode);
        if (res == null) {
            return null;
        }
        if (!origVals.containsKey(res)) {
            return "Returned TreeNode is not a node in the original tree";
        }
        if (res.val != origVals.get(res)) {
            return "Tree node values must not be modified";
        }
        return (long) origVals.get(res);
    }
}
