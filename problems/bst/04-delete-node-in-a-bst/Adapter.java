class Adapter {
    @SuppressWarnings("unchecked")
    public static Object run(Map<String, Object> inp) {
        List<Object> rawRoot = (List<Object>) inp.get("root");
        int key = ((Number) inp.get("key")).intValue();

        List<Integer> expected = new ArrayList<>();
        if (rawRoot != null) {
            for (Object o : rawRoot) {
                if (o != null) {
                    int v = ((Number) o).intValue();
                    if (v != key) {
                        expected.add(v);
                    }
                }
            }
        }
        Collections.sort(expected);

        TreeNode root = Judge.buildTree(rawRoot);
        TreeNode res = new Solution().deleteNode(root, key);

        if (expected.isEmpty()) {
            return res == null ? true : "Expected empty tree (null), got non-empty tree";
        }
        if (res == null) {
            return "Expected " + expected.size() + " nodes, got null";
        }

        Set<TreeNode> seen = Collections.newSetFromMap(new IdentityHashMap<>());
        Deque<TreeNode> stack = new ArrayDeque<>();
        TreeNode cur = res;
        List<Integer> vals = new ArrayList<>(expected.size());

        while (cur != null || !stack.isEmpty()) {
            while (cur != null) {
                if (!seen.add(cur)) {
                    return "Cycle or shared node detected in returned tree";
                }
                if (seen.size() > expected.size()) {
                    return "Returned tree has more than " + expected.size() + " nodes";
                }
                stack.push(cur);
                cur = cur.left;
            }
            TreeNode node = stack.pop();
            vals.add(node.val);
            cur = node.right;
        }

        if (vals.size() != expected.size()) {
            return "Expected " + expected.size() + " nodes, got " + vals.size();
        }
        for (int i = 1; i < vals.size(); i++) {
            if (vals.get(i) <= vals.get(i - 1)) {
                return "Returned tree is not a valid BST";
            }
        }
        if (!vals.equals(expected)) {
            return "Node values do not match expected values after deletion";
        }
        return true;
    }
}
