class Adapter {
    @SuppressWarnings("unchecked")
    public static Object run(Map<String, Object> inp) {
        List<Object> rawRoot = (List<Object>) inp.get("root");
        int pVal = ((Number) inp.get("p")).intValue();
        int qVal = ((Number) inp.get("q")).intValue();

        TreeNode root = Judge.buildTree(rawRoot);
        TreeNode pNode = null;
        TreeNode qNode = null;
        Set<TreeNode> nodes = Collections.newSetFromMap(new IdentityHashMap<>());
        Deque<TreeNode> stack = new ArrayDeque<>();
        if (root != null) {
            stack.push(root);
        }
        while (!stack.isEmpty()) {
            TreeNode node = stack.pop();
            nodes.add(node);
            if (node.val == pVal) {
                pNode = node;
            }
            if (node.val == qVal) {
                qNode = node;
            }
            if (node.left != null) {
                stack.push(node.left);
            }
            if (node.right != null) {
                stack.push(node.right);
            }
        }

        TreeNode res = new Solution().lowestCommonAncestor(root, pNode, qNode);
        if (res == null) {
            return null;
        }
        if (!nodes.contains(res)) {
            return "Returned node is not a node from the input tree";
        }
        return (long) res.val;
    }
}
