class Solution {
    private ListNode reverse(ListNode node) {
        ListNode prev = null;
        ListNode curr = node;
        while (curr != null) {
            ListNode nxt = curr.next;
            curr.next = prev;
            prev = curr;
            curr = nxt;
        }
        return prev;
    }

    public ListNode subtractSecondHalf(ListNode head) {
        if (head == null || head.next == null) {
            return head;
        }
        ListNode slow = head;
        ListNode fast = head;
        while (fast.next != null && fast.next.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        ListNode rev = reverse(slow.next);
        ListNode p1 = head;
        ListNode p2 = rev;
        while (p2 != null) {
            p1.val -= p2.val;
            p1 = p1.next;
            p2 = p2.next;
        }
        slow.next = reverse(rev);
        return head;
    }
}
