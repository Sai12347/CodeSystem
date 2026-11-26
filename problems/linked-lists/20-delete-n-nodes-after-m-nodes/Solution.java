class Solution {
    public ListNode deleteNodes(ListNode head, int m, int n) {
        ListNode curr = head;
        while (curr != null) {
            for (int i = 1; i < m; i++) {
                if (curr.next == null) {
                    return head;
                }
                curr = curr.next;
            }
            ListNode skip = curr.next;
            for (int i = 0; i < n && skip != null; i++) {
                skip = skip.next;
            }
            curr.next = skip;
            curr = skip;
        }
        return head;
    }
}
