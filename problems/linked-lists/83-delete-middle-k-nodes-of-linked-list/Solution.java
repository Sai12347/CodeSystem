class Solution {
    public ListNode deleteMiddleK(ListNode head, int k) {
        if (k == 0 || head == null) {
            return head;
        }
        ListNode dummy = new ListNode(0, head);
        ListNode cutEnd = dummy;
        for (int i = 0; i < k; i++) {
            cutEnd = cutEnd.next;
        }
        ListNode slow = dummy;
        ListNode fast = cutEnd;
        while (fast.next != null && fast.next.next != null) {
            fast = fast.next.next;
            slow = slow.next;
            cutEnd = cutEnd.next;
        }
        slow.next = cutEnd.next;
        return dummy.next;
    }
}
