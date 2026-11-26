class Solution {
    private ListNode reverse(ListNode head) {
        ListNode prev = null;
        ListNode curr = head;
        while (curr != null) {
            ListNode nxt = curr.next;
            curr.next = prev;
            prev = curr;
            curr = nxt;
        }
        return prev;
    }

    public ListNode removeNodes(ListNode head) {
        ListNode rev = reverse(head);
        int maxVal = rev.val;
        ListNode curr = rev;
        while (curr.next != null) {
            if (curr.next.val < maxVal) {
                curr.next = curr.next.next;
            } else {
                curr = curr.next;
                maxVal = curr.val;
            }
        }
        return reverse(rev);
    }
}
