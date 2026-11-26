class Solution {
    public int pathSum(TreeNode root, int targetSum) {
        Map<Long, Integer> prefix = new HashMap<>();
        prefix.put(0L, 1);
        return dfs(root, 0L, targetSum, prefix);
    }

    private int dfs(TreeNode node, long cur, int targetSum, Map<Long, Integer> prefix) {
        if (node == null) return 0;
        cur += node.val;
        int count = prefix.getOrDefault(cur - targetSum, 0);
        prefix.put(cur, prefix.getOrDefault(cur, 0) + 1);
        count += dfs(node.left, cur, targetSum, prefix);
        count += dfs(node.right, cur, targetSum, prefix);
        prefix.put(cur, prefix.get(cur) - 1);
        return count;
    }
}
