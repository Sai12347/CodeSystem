class Solution {
    private static final int NULL_SENTINEL = Integer.MIN_VALUE;

    public boolean isSubtree(TreeNode root, TreeNode subRoot) {
        List<Integer> text = new ArrayList<>();
        List<Integer> pattern = new ArrayList<>();
        serialize(root, text);
        serialize(subRoot, pattern);

        int m = pattern.size();
        int[] lps = new int[m];
        int len = 0;
        for (int i = 1; i < m; ) {
            if (pattern.get(i).equals(pattern.get(len))) {
                lps[i++] = ++len;
            } else if (len > 0) {
                len = lps[len - 1];
            } else {
                lps[i++] = 0;
            }
        }

        int j = 0;
        for (int i = 0; i < text.size(); i++) {
            Integer tok = text.get(i);
            while (j > 0 && !tok.equals(pattern.get(j))) {
                j = lps[j - 1];
            }
            if (tok.equals(pattern.get(j))) {
                j++;
                if (j == m) {
                    return true;
                }
            }
        }
        return false;
    }

    private void serialize(TreeNode node, List<Integer> out) {
        if (node == null) {
            out.add(NULL_SENTINEL);
            return;
        }
        out.add(node.val);
        serialize(node.left, out);
        serialize(node.right, out);
    }
}
