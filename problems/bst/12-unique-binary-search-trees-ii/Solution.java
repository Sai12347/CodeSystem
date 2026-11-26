class Solution {
    public List<TreeNode> generateTrees(int n) {
        if (n == 0) {
            return new ArrayList<>();
        }
        @SuppressWarnings("unchecked")
        List<TreeNode>[][] memo = new List[n + 2][n + 2];
        return build(1, n, memo);
    }

    private List<TreeNode> build(int lo, int hi, List<TreeNode>[][] memo) {
        if (lo > hi) {
            return Collections.singletonList(null);
        }
        if (memo[lo][hi] != null) {
            return memo[lo][hi];
        }
        List<TreeNode> trees = new ArrayList<>();
        for (int val = lo; val <= hi; val++) {
            List<TreeNode> lefts = build(lo, val - 1, memo);
            List<TreeNode> rights = build(val + 1, hi, memo);
            for (TreeNode left : lefts) {
                for (TreeNode right : rights) {
                    trees.add(new TreeNode(val, left, right));
                }
            }
        }
        memo[lo][hi] = trees;
        return trees;
    }
}
