class Adapter {
    @SuppressWarnings("unchecked")
    public static Object run(Map<String, Object> inp) {
        TreeNode root = Judge.buildTree((List<Object>) inp.get("root"));
        int targetVal = ((Number) inp.get("target")).intValue();
        int k = ((Number) inp.get("k")).intValue();

        TreeNode targetNode = null;
        if (root != null) {
            ArrayDeque<TreeNode> q = new ArrayDeque<>();
            q.add(root);
            while (!q.isEmpty()) {
                TreeNode node = q.poll();
                if (node.val == targetVal) {
                    targetNode = node;
                    break;
                }
                if (node.left != null) q.add(node.left);
                if (node.right != null) q.add(node.right);
            }
        }

        List<Integer> res = new Solution().distanceK(root, targetNode, k);
        if (res == null) {
            return "ERROR: expected List<Integer>, got null";
        }
        return Judge.serialize(res, "List<Integer>");
    }
}
