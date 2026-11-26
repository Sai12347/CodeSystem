class Adapter {
    @SuppressWarnings("unchecked")
    public static Object run(Map<String, Object> inp) {
        TreeNode root = Judge.buildTree((List<Object>) inp.get("root"));
        int pVal = ((Number) inp.get("p")).intValue();
        int qVal = ((Number) inp.get("q")).intValue();

        TreeNode pNode = null;
        TreeNode qNode = null;
        IdentityHashMap<TreeNode, Integer> origVals = new IdentityHashMap<>();
        if (root != null) {
            ArrayDeque<TreeNode> dq = new ArrayDeque<>();
            dq.add(root);
            while (!dq.isEmpty()) {
                TreeNode node = dq.poll();
                origVals.put(node, node.val);
                if (node.val == pVal) pNode = node;
                if (node.val == qVal) qNode = node;
                if (node.left != null) dq.add(node.left);
                if (node.right != null) dq.add(node.right);
            }
        }

        TreeNode ans = new Solution().lowestCommonAncestor(root, pNode, qNode);
        if (ans == null || !origVals.containsKey(ans)) {
            return "ERROR: returned node is null or not a node from the input tree";
        }
        if (ans.val != origVals.get(ans)) {
            return "ERROR: node value was modified";
        }
        return (long) ans.val;
    }
}
