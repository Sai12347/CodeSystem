class Solution {
    private ListNode cursor;

    public TreeNode sortedListToBST(ListNode head) {
        int n = 0;
        for (ListNode curr = head; curr != null; curr = curr.next) {
            n++;
        }
        this.cursor = head;
        return build(0, n - 1);
    }

    private TreeNode build(int lo, int hi) {
        if (lo > hi) {
            return null;
        }
        int mid = (lo + hi + 1) / 2;
        TreeNode left = build(lo, mid - 1);
        TreeNode root = new TreeNode(cursor.val);
        cursor = cursor.next;
        root.left = left;
        root.right = build(mid + 1, hi);
        return root;
    }
}
