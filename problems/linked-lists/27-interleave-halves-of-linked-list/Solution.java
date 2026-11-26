class Solution {
    public ListNode interleaveHalves(ListNode head) {
        if (head == null || head.next == null) {
            return head;
        }
        ListNode slow = head;
        ListNode fast = head.next;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        ListNode second = slow.next;
        slow.next = null;
        ListNode first = head;
        while (second != null) {
            ListNode nxt1 = first.next;
            ListNode nxt2 = second.next;
            first.next = second;
            second.next = nxt1;
            first = nxt1;
            second = nxt2;
        }
        return head;
    }
}
