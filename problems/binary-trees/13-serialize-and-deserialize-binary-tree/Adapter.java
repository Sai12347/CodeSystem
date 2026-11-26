class Adapter {
    @SuppressWarnings("unchecked")
    public static Object run(Map<String, Object> inp) {
        TreeNode orig = Judge.buildTree((List<Object>) inp.get("root"));
        List<Object> origJson = Judge.treeToJson(orig);
        IdentityHashMap<TreeNode, Boolean> origSet = new IdentityHashMap<>();
        if (orig != null) {
            ArrayDeque<TreeNode> q = new ArrayDeque<>();
            q.add(orig);
            while (!q.isEmpty()) {
                TreeNode node = q.poll();
                origSet.put(node, Boolean.TRUE);
                if (node.left != null) q.add(node.left);
                if (node.right != null) q.add(node.right);
            }
        }

        String ser = new Codec().serialize(orig);
        if (ser == null) {
            return "ERROR: serialize must return a non-null String";
        }
        if (!Judge.treeToJson(orig).equals(origJson)) {
            return "ERROR: serialize must not modify the input tree";
        }

        TreeNode deser = new Codec().deserialize(ser);
        if (deser != null) {
            IdentityHashMap<TreeNode, Boolean> seen = new IdentityHashMap<>();
            ArrayDeque<TreeNode> q = new ArrayDeque<>();
            q.add(deser);
            while (!q.isEmpty()) {
                TreeNode node = q.poll();
                if (origSet.containsKey(node)) {
                    return "ERROR: deserialize must construct new TreeNode objects, not reuse original nodes";
                }
                if (seen.put(node, Boolean.TRUE) != null) {
                    return "ERROR: deserialized tree contains a cycle or shared node";
                }
                if (seen.size() > 100_000) {
                    return "ERROR: deserialized tree is too large";
                }
                if (node.left != null) q.add(node.left);
                if (node.right != null) q.add(node.right);
            }
        }

        return Judge.treeToJson(deser);
    }
}
