class Solution {
    private int preIdx;
    private Map<Integer, Integer> inIndex;

    public TreeNode buildTree(int[] preorder, int[] inorder) {
        inIndex = new HashMap<>(inorder.length * 2);
        for (int i = 0; i < inorder.length; i++) {
            inIndex.put(inorder[i], i);
        }
        preIdx = 0;
        return helper(preorder, 0, inorder.length - 1);
    }

    private TreeNode helper(int[] preorder, int left, int right) {
        if (left > right) {
            return null;
        }
        int rootVal = preorder[preIdx++];
        TreeNode root = new TreeNode(rootVal);
        int mid = inIndex.get(rootVal);
        root.left = helper(preorder, left, mid - 1);
        root.right = helper(preorder, mid + 1, right);
        return root;
    }
}
